from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from expense_manager.models import *
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from django.core.mail import send_mail
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view


class AddExpenseView(APIView):
    def post(self, request):
        description = request.data.get("description")
        amount = Decimal(request.data.get("amount"))
        participants = request.data.get("participants")

        try:
            with transaction.atomic():
                # Create a new Expense object
                expense = Expense(description=description, amount=amount)
                expense.save()

                # Calculate shares per participant
                share_per_participant = amount / len(participants)

                # Create ExpenseParticipant objects for each participant
                for participant_name in participants:
                    try:
                        participant = User.objects.get(name=participant_name)
                        ep = ExpenseParticipant(
                            user=participant,
                            expense=expense,
                            paid_share=share_per_participant,
                            owe_share=share_per_participant,
                        )
                        ep.save()
                    except User.DoesNotExist:
                        return Response(
                            {
                                "error": f"Participant with name '{participant_name}' not found"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # Update balances for each participant
                for participant_name in participants:
                    participant = User.objects.get(name=participant_name)
                    participant_balances = ExpenseParticipant.objects.filter(
                        user=participant, expense=expense
                    )
                    total_paid_share = sum(
                        [ep.paid_share for ep in participant_balances]
                    )
                    total_owe_share = sum([ep.owe_share for ep in participant_balances])
                    balance = total_paid_share - total_owe_share
                    participant.balance = balance
                    participant.save()

                return Response({"success": True}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def view_balances(request):
    users = User.objects.all()
    balances = {}

    for user in users:
        participant_balances = ExpenseParticipant.objects.filter(user=user)

        total_paid_share = participant_balances.aggregate(total_paid=Sum("paid_share"))[
            "total_paid"
        ] or Decimal("0.00")
        total_owe_share = participant_balances.aggregate(total_owe=Sum("owe_share"))[
            "total_owe"
        ] or Decimal("0.00")

        balance = total_paid_share - total_owe_share
        print(balances)

        balance = round(balance, 2)
        balances[user.name] = balance

    # Create a list of user names and balances as dictionaries
    balances_data = [
        {"user": user, "balance": str(balances[user])} for user in balances.keys()
    ]
    # Return the data as JSON
    return JsonResponse(balances_data, safe=False)


@api_view(["POST"])
def send_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        amount = serializer.validated_data["amount"]

        # Customize the email subject and message
        subject = "Notification Subject"
        message = f"You owe ${amount} for the expense."

        # Send the email
        send_mail(subject, message, "your_email@example.com", [email])

        return Response(
            {"message": "Notification sent successfully"},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
