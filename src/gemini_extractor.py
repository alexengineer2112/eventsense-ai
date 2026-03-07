import os
import json
import re
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=api_key)


def extract_multiple_emails(emails):

    combined_text = ""

    for i, email in enumerate(emails, start=1):
        combined_text += f"\n\nEMAIL {i}:\n{email}\n"

    prompt = f"""
You are an AI assistant that extracts placement opportunity information from university emails.

Analyze EACH email carefully.

Return ONLY valid JSON.

Do NOT include explanations.
Do NOT include markdown.
Do NOT include extra text.

Required fields:

category
company
job_role
deadline
application_links

Category must be one of:
- Internship
- Full-Time Opportunity
- Campus Recruitment
- Workshop
- General

If information is missing return "Not Found".

Return format:

[
 {{
  "category": "",
  "company": "",
  "job_role": "",
  "deadline": "",
  "application_links": []
 }}
]

Emails:
{combined_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text_output = response.text.strip()

        # Remove markdown if Gemini adds it
        text_output = re.sub(r"```json|```", "", text_output).strip()

        data = json.loads(text_output)

        return data

    except Exception as e:

        print("⚠️ Error while processing emails with Gemini")
        print(e)

        return None