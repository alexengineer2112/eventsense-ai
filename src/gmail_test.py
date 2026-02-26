import os
import base64
import pickle
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Import your NLP logic
from main import (
    classify_email,
    extract_deadline,
    extract_company,
    extract_job_role,
    extract_links
)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_email_body(message):
    """Extract and decode email body"""
    try:
        payload = message['payload']
        parts = payload.get('parts')

        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8')

    except Exception:
        return ""


def main():
    creds = None

    # Load existing token if available
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)

    # If no valid token, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    # Build Gmail service
    service = build('gmail', 'v1', credentials=creds)

    print("\n🔎 Searching for placement/internship emails...\n")

    results = service.users().messages().list(
        userId='me',
        q="internship OR placement OR recruitment OR full-time",
        maxResults=5
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("No relevant emails found.")
        return

    for msg in messages:

        # Get full message
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        # Extract issued date
        internal_date = int(msg_data['internalDate'])
        issued_date = datetime.fromtimestamp(internal_date / 1000)

        # Extract email body
        body = get_email_body(msg_data)

        if not body:
            continue

        # Run NLP extraction
        category = classify_email(body)
        deadline = extract_deadline(body)
        company = extract_company(body)
        job_role = extract_job_role(body)
        links = extract_links(body)

        # Print structured output
        print("📧 Email Processed")
        print("Category      :", category)
        print("Issued Date   :", issued_date.strftime("%d-%m-%Y"))
        print("Deadline      :", deadline)
        print("Company       :", company)
        print("Job Role      :", job_role)

        if links:
            print("Links Found   :", len(links))
            for link_type, link in links:
                print(f" - {link_type}: {link}")
        else:
            print("Links Found   : None")

        print("-" * 60)


if __name__ == "__main__":
    main()