from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_notification_email(participants, subject, message):
    for email in participants:
        subject = "Weekly Reminder"  # Customize the subject
        message = "Here is a summary of amounts you owe to other users:\n"  # Customize the message

        # You can include additional data or formatting in the message
        message += "User 1: $50\n"
        message += "User 2: $30\n"
        message += "User 3: $20\n"

        # Send the customized email
        send_mail(subject, message, "your_email@example.com", [email])
