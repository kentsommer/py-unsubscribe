# Automatic email unsubscriber in Python (Currently only supports Gmail)

## Get an API Client ID and Secret

1. Use [this wizard](https://console.developers.google.com/start/api?id=gmail) to create or select a project in the Google Developers Console and automatically turn on the API. Click **Continue**, then **Go to credentials**.
2. On the **Add credentials to your project** page, click the **Cancel** button.
3. At the top of the page, select the **OAuth consent screen** tab. Select an **Email address**, enter a **Product name** if not already set, and click the Save button.
4. Select the **Credentials** tab, click the **Create credentials** button and select **OAuth client ID**.
5. Select the application type **Other**, enter the name "Unsubscribe", and click the **Create** button.
6. Click **OK** to dismiss the resulting dialog.
7. Click the Download button to the right of the client ID.
8. Move this file to your working directory and rename it ```client_secret.json```.

## Usage Instructions
1. Label any message in Gmail that you want to be unsubscribed from with the label "Unsubscribe"
2. Run: ```pip install -r reqs.txt```
3. Run: ```python gmail_unsubscribe.py```

## Output Explanation
1. "Unsubscribed from: Sender_Name" -> Unsubscription was successful (Finished work)
2. "Could not unsubscribe: Sender_name" -> There was no unsubscribe link in the header (Nothing to do)
3. "Already Unsubscribed from: Sender_name" -> Already unsubscribed successfully during this session (Skipping)
4. "Finished Cleanup" -> Removed the "Unsubscribe" label and deleted the message
