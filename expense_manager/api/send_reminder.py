from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from expense_manager.models import *
from decimal import Decimal


class Command(BaseCommand):
    help = "Send weekly reminder emails to users about amounts they owe."
    def handle(self, *args, **options):
        users = User.objects.all()
        amounts_owed = {}
        for user in users:
            user_owed = Decimal(0)
            user_expenses = ExpenseParticipant.objects.filter(user=user)
            for expense in user_expenses:
                user_owed += expense.owe_share
            amounts_owed[user.name] = user_owed
        subject = "Weekly Reminder"
        message = "Here is a summary of amounts you owe to other users:\n"
        for user, amount in amounts_owed.items():
            message += f"{user}: ${amount}\n"
        send_mail(subject, message, "your_email@example.com", [user_email])
