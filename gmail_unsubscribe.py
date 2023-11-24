"""
Unsubscribes from any email labeled "Unsubscribe"
As long as the email contains the List Unsubscribe header
"""
import base64
import quopri
import re
import os
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if not os.path.isfile('credentials.json'):
    logging.critical("🚫 Credentials file not found. Please ensure 'credentials.json' exists.")
    exit()
if not os.path.isfile('client_secret.json'):
    logging.critical("🚫 Client secrets file not found. Please ensure 'client_secret.json' exists.")
    exit()

def get_gmail_service():
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    logging.info("✅ Gmail service initialized successfully")
    return service

def get_label_id(service, label_name):
    try:
        results = service.users().labels().list(userId='me').execute()
        for label in results.get('labels', []):
            if label['name'] == label_name:
                return label['id']
        return '-1'
    except HttpError as error:
        logging.error(f"🚫 An error occurred finding the label id: {error}")

def get_messages_with_label(service, label_id):
    try:
        response = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
        return response.get('messages', [])
    except HttpError as error:
        logging.error(f"🚫 An error occurred finding messages: {error}")

def get_message(service, msg_id):
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII')).decode('utf-8', 'ignore')
        return msg_str
    except HttpError as error:
        logging.error(f"🚫 An error occurred getting a message: {error}")

def unsubscribe(service, messages, label_id):
    for item in messages:
        msg_id = item['id']
        msg_str = get_message(service, msg_id)
        url = get_unsubscribe_url(msg_str)
        if url:
            try:
                response = requests.get(url, timeout=10)
                logging.info(f"✅ Unsubscribed from: {url}")
                unlabel_message(service, msg_id, label_id)
                delete_message(service, msg_id)
            except requests.exceptions.RequestException as e:
                logging.warning(f"⚠️ Unsubscribe attempt failed for {url}: {e}")
        else:
            logging.info("🔍 No unsubscribe link found. Skipping message.")

if __name__ == '__main__':
    gmail = get_gmail_service()
    label = 'Unsubscribe'
    label_id = get_label_id(gmail, label)
    if label_id != '-1':
        messages = get_messages_with_label(gmail, label_id)
        if messages:
            unsubscribe(gmail, messages, label_id)
        else:
            logging.info("✅ No messages to unsubscribe from.")
    else:
        logging.warning("⚠️ Unsubscribe label not found.")
