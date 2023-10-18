from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("ragister/",views.add_user),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('view_balances/', views.view_balances, name='view_balances'),
    path('view_balances/<int:user_id>/', views.view_balances, name='view_user_balance'),

    path('split_equally/', views.split_equally, name='split_equally'),
    path('split_equally/success/', views.split_equally_success, name='split_equally_success'),
    path('split_exact/', views.split_exact, name='split_exact'),

    # path('send_reminders/', views.send_reminders, name='send_reminders'),
]
