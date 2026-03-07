from datetime import datetime
from dateutil import parser


def analyze_deadline(deadline_text):

    if deadline_text == "Not Found":
        return {
            "deadline_date": "Unknown",
            "days_left": "Unknown",
            "urgency": "Unknown"
        }

    try:
        deadline_date = parser.parse(deadline_text)

        today = datetime.now()

        days_left = (deadline_date - today).days

        if days_left < 0:
            urgency = "Expired"

        elif days_left == 0:
            urgency = "Very Urgent"

        elif days_left <= 2:
            urgency = "Urgent"

        elif days_left <= 7:
            urgency = "High"

        else:
            urgency = "Normal"

        return {
            "deadline_date": deadline_date.strftime("%Y-%m-%d"),
            "days_left": days_left,
            "urgency": urgency
        }

    except:
        return {
            "deadline_date": deadline_text,
            "days_left": "Unknown",
            "urgency": "Unknown"
        }