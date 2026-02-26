import spacy
nlp = spacy.load("en_core_web_sm")
import re
from datetime import datetime


def classify_email(text):
    text = text.lower()

    if "campus recruitment" in text:
        return "Campus Recruitment Opportunity"
    elif "full-time" in text or "full time" in text:
        return "Full-Time Opportunity"
    elif "internship" in text:
        return "Internship"
    elif "placement drive" in text:
        return "Placement Drive"
    elif "recruitment" in text:
        return "Recruitment Opportunity"
    else:
        return "General"



def extract_deadline(text):
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "DATE":
            return ent.text

    return "Not Found"


def extract_company(text):
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text

    return "Not Found"


def extract_job_role(text):
    match = re.search(r'role\s+(?:of|:)?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
    return match.group(1).strip() if match else "Not Found"


def extract_links(text):
    links = re.findall(r'https?://[^\s]+', text)

    classified_links = []

    for link in links:
        if "forms.gle" in link or "google.com/forms" in link:
            classified_links.append(("Google Form", link))
        else:
            classified_links.append(("Official/Other Link", link))

    return classified_links