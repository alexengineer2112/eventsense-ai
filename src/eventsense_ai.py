from gmail_reader import fetch_placement_emails
from gemini_extractor import extract_multiple_emails


def main():

    print("\n🔎 Fetching latest placement emails...\n")

    emails = fetch_placement_emails()

    if not emails:

        print("No placement emails found.")
        return

    results = extract_multiple_emails(emails)

    if not results:
        print("AI extraction failed.")
        return

    for i, result in enumerate(results, start=1):

        print(f"\n📧 Email {i}")

        print("Category :", result.get("category"))
        print("Company  :", result.get("company"))
        print("Job Role :", result.get("job_role"))
        print("Deadline :", result.get("deadline"))
        

        print("-" * 50)


if __name__ == "__main__":
    main()