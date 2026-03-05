from google import genai
import json

API_KEY = "AIzaSyA4w3ZFvQ0y7vKXfVFPjvr5gPidqdcPwnQ"

client = genai.Client(api_key=API_KEY)


def extract_multiple_emails(emails):

    combined_text = ""

    for i, email in enumerate(emails, start=1):
        combined_text += f"\n\nEMAIL {i}:\n{email}\n"

    prompt = f"""
You are an AI system that extracts placement information from university emails.

Extract information from EACH email.

Return ONLY JSON list.

Format:

[
 {{
  "category": "",
  "company": "",
  "job_role": "",
  "deadline": "",
    }}
]

Emails:
{combined_text}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    text_output = response.text.strip()

    try:
        data = json.loads(text_output)
        return data

    except:
        print("⚠️ JSON parsing failed")
        print(text_output)
        return None