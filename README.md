# Gmail Automatic Unsubscription Tool

This tool automates the process of unsubscribing from emails directly within Gmail using the Gmail API.

## Setup

### Step 1: Google API Credentials
- Go to the [Google Developers Console](https://console.developers.google.com/start/api?id=gmail).
- Create or select a project.
- Enable the Gmail API and go to `Credentials`.
- In the `OAuth consent screen`, provide the necessary product details.
- In the `Credentials` tab, create a new `OAuth client ID`.
- Select the `Other` application type, name it "Unsubscribe".
- Download your client ID and rename it to `client_secret.json`, place it in your project directory.

### Step 2: Installation
- Label emails to unsubscribe with "Unsubscribe" in Gmail.
- Install dependencies: `pip install -r requirements.txt`

### Step 3: Execution
- Run the script: `python gmail_unsubscribe.py`

## What to Expect

### Outputs
- "Unsubscribed from: Sender_Name": Success.
- "Could not unsubscribe: Sender_name": No link found.
- "Already Unsubscribed from: Sender_name": Previously processed.
- "Finished Cleanup": Labels and messages removed.

## Contributing

Feel free to fork the project, submit pull requests, or send suggestions to improve the script.

---

Your feedback and contributions are welcome!
