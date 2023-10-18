from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import *
from django.contrib.auth.hashers import make_password
from django.db import transaction


def index(request):
    return render(request, "index.html")


def add_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        if User.objects.filter(email=email).exists():
            return HttpRequest("Email already Ragister")
        elif User.objects.filter(mobile_number=mobile).exists():
            return HttpRequest("Mobile Number already Ragister")
        else:
            User.objects.create(name=name, email=email, mobile_number=mobile)
    return render(request, "add_user.html")


def add_expense(request):
    if request.method == "POST":
        description = request.POST.get("description")
        amount = Decimal(request.POST.get("amount"))
        participants = request.POST.getlist("participants")

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
                        # Handle the case where a participant with the given name is not found
                        return JsonResponse(
                            {
                                "error": f"Participant with name '{participant_name}' not found"
                            }
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

                # return JsonResponse({"success": True})
                return redirect("view_balances")

        except Exception as e:
            # Handle database transaction errors or other exceptions
            return JsonResponse({"error": str(e)})

    else:
        # Retrieve all users from the database
        users = User.objects.all()
        return render(request, "add_expense.html", context={"users": users})


def view_balances(request, user_id=None):
    users = User.objects.all()
    balances = {}

    if user_id is not None:
        # Retrieve a specific user by ID or name
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse("User not found")

        # Calculate the balance for the specific user
        participant_balances = ExpenseParticipant.objects.filter(user=user)
        total_paid_share = sum([ep.paid_share for ep in participant_balances])
        total_owe_share = sum([ep.owe_share for ep in participant_balances])
        balance = total_paid_share - total_owe_share

        # Add the specific user's balance to the balances dictionary
        balances[user.name] = balance
    else:
        for user in users:
            participant_balances = ExpenseParticipant.objects.filter(user=user)
            total_paid_share = sum([ep.paid_share for ep in participant_balances])
            total_owe_share = sum([ep.owe_share for ep in participant_balances])
            balance = total_paid_share - total_owe_share
            balances[user.name] = balance

    print("Users:", users)
    print("Balances:", balances)
    return render(request, "view_balances.html", context={"balances": balances, "user":users})



def split_equally(request):
    if request.method == "POST":
        payer_name = request.POST.get("payer_name")
        amount = Decimal(request.POST.get("amount"))
        participants = request.POST.getlist("participants")

        # Calculate shares per participant
        if len(participants) > 0:
            share_per_participant = amount / len(participants)
        else:
            # Handle the case where there are no participants to split the expense
            share_per_participant = Decimal("0.00")

        try:
            with transaction.atomic():
                # Create a new Expense object
                expense = Expense(description="Split Equally Expense", amount=amount)
                expense.save()

                # Update balances for each participant
                for participant_name in participants:
                    try:
                        participant = User.objects.get(name=participant_name)
                        participant_balance = ExpenseParticipant.objects.filter(
                            user=participant
                        )
                        payer = User.objects.get(name=payer_name)

                        if not participant_balance.exists():
                            # If the participant doesn't have any balance entry, create one
                            ExpenseParticipant.objects.create(
                                user=participant,
                                expense=expense,
                                paid_share=Decimal(0),
                                owe_share=share_per_participant,
                            )
                        else:
                            # Update balances for payer
                            payer_balance = ExpenseParticipant.objects.get(
                                user=payer, expense=expense
                            )
                            payer_balance.owe_share -= share_per_participant
                            payer_balance.save()

                            # Update balances for participants
                            participant_balance = participant_balance[0]
                            participant_balance.owe_share += share_per_participant
                            participant_balance.save()
                    except User.DoesNotExist:
                        # Handle the case where a participant with the given name is not found
                        return JsonResponse(
                            {
                                "error": f"Participant with name '{participant_name}' not found"
                            }
                        )

                return render(request, "split_equally_success.html")

        except Exception as e:
            # Handle database transaction errors or other exceptions
            return JsonResponse({"error": str(e)})

    else:
        users = User.objects.all()
        return render(request, "split_equally.html", context={"users": users})


def split_equally_success(request):
    return render(request, "split_equally_success.html")


def split_exact(request):
    if request.method == "POST":
        payer_id = request.POST.get("payer")
        amount = request.POST.get("amount")
        owes_data = request.POST.get("owes_data")

        # Validate the 'amount' and 'owes_data' formats
        try:
            amount = Decimal(amount)
            owes_data = [Decimal(owe) for owe in owes_data.split(",")]

            # Calculate total owed amount
            total_owed = sum(owes_data)
        except (ValueError, InvalidOperation):
            # Handle the case where an invalid format is provided
            return HttpResponse(
                "Invalid format in 'amount' or 'owes_data'. Please use valid decimal numbers."
            )

        # Create a new expense
        expense = Expense(description="Custom Expense", amount=amount)
        expense.save()

        # Update balances for payer
        payer = User.objects.get(id=payer_id)
        payer_balance, created = ExpenseParticipant.objects.get_or_create(
            user=payer, expense=expense
        )
        if created:
            payer_balance.paid_share = amount
            payer_balance.owe_share = total_owed
        else:
            payer_balance.paid_share += amount
            payer_balance.owe_share += total_owed
        payer_balance.save()

        # Update balances for those who owe
        for user_id, owe_amount in zip(request.POST.getlist("participants"), owes_data):
            user = User.objects.get(id=user_id)
            user_balance, created = ExpenseParticipant.objects.get_or_create(
                user=user, expense=expense
            )
            user_balance.paid_share = Decimal(0)
            user_balance.owe_share = owe_amount
            user_balance.save()

        return redirect("view_balances")
    else:
        users = User.objects.all()
        return render(request, "split_exact.html", context={"users": users})
