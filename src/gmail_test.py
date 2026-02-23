import os
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle

print("Script started")
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None

    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me', maxResults=5).execute()

    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print('Last 5 emails:')
        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me', id=msg['id']).execute()
            snippet = msg_data['snippet']
            print("-", snippet)

if __name__ == '__main__':
    main()