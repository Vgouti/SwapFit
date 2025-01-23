from django.urls import path
from .views import user_transactions

urlpatterns = [
    path('', user_transactions, name='user_transactions'),
]
