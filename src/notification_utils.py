from plyer import notification


def send_notification(title, message):

    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )

    except Exception as e:
        print("Notification error:", e)