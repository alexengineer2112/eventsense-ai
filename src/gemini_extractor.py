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
    You analyze placement office emails from a university.

    Two types of emails exist:

    1. Placement Opportunity
    2. General Announcement / Information

    Return a JSON ARRAY where each element corresponds to one email.

    Opportunity format:

    {{
    "type": "opportunity",
    "company": "",
    "job_role": "",
    "deadline": "",
    "application_links": []
    }}

    Announcement format:

    {{
    "type": "announcement",
    "summary": "brief 1-2 sentence summary"
    }}

    Rules:
    - Only include fields that exist
    - If deadline is missing, omit it
    - Do NOT return explanations
    - Return ONLY JSON ARRAY

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