from gmail_reader import fetch_placement_emails
from gemini_extractor import extract_multiple_emails
from deadline_utils import analyze_deadline
from notification_utils import send_notification

import json
import os


DATA_FILE = "data/placement_results.json"
PROCESSED_FILE = "data/processed.json"


def load_processed_emails():

    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)

    return []


def save_processed_emails(ids):

    with open(PROCESSED_FILE, "w") as f:
        json.dump(ids, f, indent=4)


def main():

    print("\n🔎 Fetching latest placement emails...\n")

    emails = fetch_placement_emails()

    print(f"Total emails fetched: {len(emails)}")

    processed_ids = load_processed_emails()

    new_emails = []

    for email in emails:

        if email["id"] not in processed_ids:
            new_emails.append(email)
            processed_ids.append(email["id"])

    if not new_emails:
        print("No new emails to analyze.")
        return

    print(f"New emails detected: {len(new_emails)}")

    email_contents = [email["content"] for email in new_emails]

    print("Sending emails to Gemini...\n")

    results = extract_multiple_emails(email_contents)

    if not results:
        print("AI extraction failed.")
        return

    cleaned_results = []

    for job in results:

        deadline = job.get("deadline")

        # Analyze deadline only if it exists
        if deadline and deadline != "Not Found":
            job["deadline_status"] = analyze_deadline(deadline)

        else:
            job.pop("deadline", None)

        cleaned_results.append(job)

        # ------------------------
        # Console Output
        # ------------------------

        print("\n📧 Email")

        if job.get("company"):
            print("Company :", job.get("company"))

        if job.get("job_role"):
            print("Role    :", job.get("job_role"))

        if job.get("deadline"):
            print("Deadline:", job.get("deadline"))

            if job.get("deadline_status"):
                print("Status  :", job.get("deadline_status"))

        if job.get("summary"):
            print("Info    :", job.get("summary"))

        print("-" * 50)

        # ------------------------
        # Desktop Notification
        # ------------------------

        if job.get("type") == "opportunity" and job.get("company"):

            message = job.get("company")

            if job.get("job_role"):
                message += f" - {job.get('job_role')}"

            send_notification(
                title="New Placement Opportunity",
                message=message
            )

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(cleaned_results, f, indent=4, ensure_ascii=False)

    save_processed_emails(processed_ids)

    print("\n✅ Results saved to data/placement_results.json")


if __name__ == "__main__":
    main()