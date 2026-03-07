import json
from gmail_reader import fetch_emails
from gemini_extractor import extract_multiple_emails
from deadline_utils import analyze_deadline
from notification_utils import send_notification


PROCESSED_FILE = "data/processed.json"


def load_processed():

    try:
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)

    except:
        return []


def save_processed(ids):

    with open(PROCESSED_FILE, "w") as f:
        json.dump(ids, f)


def main():

    print("\n🔎 Fetching latest placement emails...\n")

    processed_ids = load_processed()

    emails = fetch_emails()

    email_contents = []
    new_ids = []

    for email in emails:

        email_id = email["id"]

        if email_id not in processed_ids:

            email_contents.append(email["content"])
            new_ids.append(email_id)

    print("Total emails fetched:", len(emails))
    print("New emails detected:", len(email_contents))

    if not email_contents:

        print("✅ No new placement emails\n")
        return

    print("Sending emails to Gemini...\n")

    results = extract_multiple_emails(email_contents)

    if not results:
        print("⚠️ No results returned from AI")
        return

    for job in results:

        deadline_info = analyze_deadline(job["deadline"])

        job["deadline_date"] = deadline_info["deadline_date"]
        job["days_left"] = deadline_info["days_left"]
        job["urgency"] = deadline_info["urgency"]

        print("\n📌 Opportunity Found")
        print("Company:", job["company"])
        print("Role:", job["job_role"])
        print("Deadline:", job["deadline_date"])
        print("Urgency:", job["urgency"])

        # send desktop notification
        send_notification(
            job["company"],
            job["deadline_date"],
            job["urgency"]
        )

    processed_ids.extend(new_ids)

    save_processed(processed_ids)

    print("\n✅ Emails processed successfully\n")