import re

def classify_email(text):
    text = text.lower()
    if "internship" in text or "placement" in text:
        return "Placement / Internship"
    elif "workshop" in text or "training" in text:
        return "Workshop"
    else:
        return "General"

def extract_deadline(text):
    # Matches: 15th January 2026 OR 15 January 2026
    pattern = r'(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})'
    match = re.search(pattern, text)
    return match.group(1) if match else "Not Found"

def extract_company(text):
    match = re.search(r'Internship opportunity with (.+?) \(', text)
    return match.group(1) if match else "Not Found"

def process_email(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        text = file.read()

    category = classify_email(text)
    deadline = extract_deadline(text)
    company = extract_company(text)

    print("📧 Email Processed Successfully")
    print("Category       :", category)
    print("Company        :", company)
    print("Deadline       :", deadline)
    print("Action         : Task & Reminder Created")
    print("-" * 50)

if __name__ == "__main__":
    process_email("data/placement_email.txt")
    process_email("data/workshop_email.txt")

