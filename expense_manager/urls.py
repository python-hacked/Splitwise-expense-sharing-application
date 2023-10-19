from django.urls import path
from . import views
from .api.api import AddExpenseView
from .api import api

urlpatterns = [
    path("", views.index),
    path("ragister/", views.add_user),
    path("add_expense/", views.add_expense, name="add_expense"),
    path("view_balances/", views.view_balances, name="view_balances"),
    # path('view_balances/<int:user_id>/', views.view_balances, name='view_balances'),
    path("split_equally/", views.split_equally, name="split_equally"),
    path(
        "split_equally/success/",
        views.split_equally_success,
        name="split_equally_success",
    ),
    path("split_exact/", views.split_exact, name="split_exact"),
    path("send_email/", views.send_email, name="send_email"),
    # API URL
    path("api/add_expense/", AddExpenseView.as_view(), name="add_expense"),
    path("api/view_balances/", api.view_balances, name="api_view_balances"),
    path("api/send_notification/", api.send_notification, name="send_notification"),
    # path('send_reminders/', views.send_reminders, name='send_reminders'),
]
