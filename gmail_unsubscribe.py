"""
Unsubscribes from any email labeled "Unsubscribe"
As long as the email contains the List Unsubscribe header
"""
from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import quopri
import re
import urlfetch


def get_gmail_service():
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service


def get_label_id(service, label_name):
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        for label in labels:
            if label['name'] == label_name:
                return label['id']
        return '-1'
    except errors.HttpError as error:
        print('An error occurred finding the label id: %s' % error)


def get_messages_with_label(service, label_id):
    try:
        message_dict = service.users().messages().list(userId='me', labelIds=[label_id,]).execute()
        messages = message_dict['messages']
        return messages
    except errors.HttpError as error:
        print('An error occurred finding messages: %s' % error)


def get_message(service, msg_id):
    try:
        message = service.users().messages().get(userId='me', id=msg_id,
                                             format='raw').execute()
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII')).decode('utf-8')
        return msg_str
    except errors.HttpError as error:
        print('An error occurred getting a message: %s' % error)


def decode_mime(msg_str):
    pattern = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
    match = re.search(pattern, msg_str)
    if match:
        charset, encoding, text = match.groups()
        if encoding is 'B':
            byte_string = base64.b64decode(text)
        elif encoding is 'Q':
            byte_string = quopri.decodestring(text)
        return byte_string.decode(charset)
    else:
        return msg_str


def get_sender(msg_str):
    pattern = re.compile(r"^from:(.*?)\<", re.M | re.I)
    match = pattern.search(msg_str)
    if match:
        sender = decode_mime(match.group(1))
        return sender
    return match


def get_unsubscribe_url(msg_str):
    pattern = re.compile(r"^list\-unsubscribe:(.|\r\n\s)+<(https?:\/\/[^>]+)>", re.M | re.I)
    match = pattern.search(msg_str)
    if match:
        return match.group(2)
    return match


def unlabel_message(service, msg_id, label_id):
    service.users().messages().modify(userId='me', id=msg_id, body={ 'removeLabelIds': [label_id,]}).execute()


def delete_message(service, msg_id):
    service.users().messages().trash(userId='me', id=msg_id).execute()


def unsubscribe(service, messages, label_id):
    for item in messages:
        msg_id = item['id']
        msg = get_message(service, msg_id)
        url = get_unsubscribe_url(msg)
        if url:
            sender = get_sender(msg).strip().replace("\"", '')
            response = urlfetch.get(url)
            unlabel_message(service, msg_id, label_id)
            delete_message(service, msg_id)
            print("Unsubscribed from: {}".format(sender))



if __name__ == '__main__':
    # Set label
    label = 'Unsubscribe'
    # Get Service
    gmail = get_gmail_service()
    # Get Unsubscribe Label ID
    label_id = get_label_id(gmail, label)
    # Get Unsubscribe messages
    messages = get_messages_with_label(gmail, label_id)
    while len(messages) > 0:  
        # Unsubscribe
        unsubscribe(gmail, messages, label_id)
        messages = get_messages_with_label(gmail, label_id)
