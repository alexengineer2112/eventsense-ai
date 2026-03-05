import base64
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def gmail_authenticate():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service


def get_email_body(payload):

    if "parts" in payload:

        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode()

    if payload["body"].get("data"):

        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode()

    return ""


def fetch_placement_emails():

    service = gmail_authenticate()

    query = "from:placementoffice.soet@christuniversity.in"

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:

        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        payload = msg_data["payload"]
        headers = payload["headers"]

        subject = ""

        for header in headers:

            if header["name"] == "Subject":
                subject = header["value"]

        body = get_email_body(payload)

        email_text = subject + "\n" + body

        email_text = email_text[:1200]  # token optimization

        emails.append(email_text)

    return emails