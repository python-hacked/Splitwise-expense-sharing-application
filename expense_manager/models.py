from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)

class Expense(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class ExpenseParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    paid_share = models.DecimalField(max_digits=10, decimal_places=2)
    owe_share = models.DecimalField(max_digits=10, decimal_places=2)
