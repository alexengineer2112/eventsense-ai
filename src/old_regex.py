import re
import spacy

nlp = spacy.load("en_core_web_sm")


# ---------------- CATEGORY ---------------- #

def classify_email(text):
    text = text.lower()

    if "campus recruitment" in text:
        return "Campus Recruitment Opportunity"
    elif "placement drive" in text:
        return "Placement Drive"
    elif "full-time" in text or "full time" in text:
        return "Full-Time Opportunity"
    elif "internship" in text:
        return "Internship"
    elif "trainee" in text:
        return "Trainee Opportunity"
    elif "recruitment" in text:
        return "Recruitment Opportunity"
    else:
        return "General"


# ---------------- COMPANY ---------------- #

def extract_company(text, subject):

    # 1️⃣ Pattern: opportunity with XYZ
    match = re.search(r'opportunity with ([A-Za-z0-9 &.,]+)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # 2️⃣ Pattern: recruitment by XYZ
    match = re.search(r'recruitment (?:drive )?with ([A-Za-z0-9 &.,]+)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # 3️⃣ Try extracting from subject (after dash)
    match = re.search(r'-\s*(.+)', subject)
    if match:
        return match.group(1).strip()

    # 4️⃣ Try extracting from official job link (like iqvia.wd1...)
    link_match = re.search(r'https?://([A-Za-z0-9\-]+)\.', text)
    if link_match:
        domain_name = link_match.group(1)
        if domain_name.lower() not in ["docs", "forms", "google"]:
            return domain_name.upper()

    return "Not Found"

# ---------------- DEADLINE ---------------- #

def extract_deadline(text):
    keywords = ["deadline", "last date", "apply before", "closing date"]

    text_lower = text.lower()

    if any(word in text_lower for word in keywords):
        match = re.search(r'\d{1,2}.*?\d{4}', text)
        if match:
            return match.group()

    return "Not Found"


# ---------------- JOB ROLE ---------------- #

def extract_job_role(text):
    patterns = [
        r'role of ([A-Za-z\s]+)',
        r'position of ([A-Za-z\s]+)',
        r'for the role of ([A-Za-z\s]+)',
        r'for the position of ([A-Za-z\s]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return "Not Found"


# ---------------- LINKS ---------------- #

def extract_links(text):
    links = re.findall(r'https?://[^\s<>"*]+', text)

    clean_links = []
    for link in links:
        if "unsubscribe" in link.lower():
            continue
        if "mypreferences" in link.lower():
            continue
        if "help" in link.lower():
            continue

        if "forms.gle" in link or "google.com/forms" in link:
            clean_links.append(("Google Form", link))
        else:
            clean_links.append(("Official Link", link))

    return clean_links