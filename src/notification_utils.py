from plyer import notification

def send_notification(company, deadline, urgency):

    title = "📢 Placement Opportunity"

    message = f"""
Company: {company}
Deadline: {deadline}
Urgency: {urgency}
"""

    notification.notify(
        title=title,
        message=message,
        timeout=10
    )