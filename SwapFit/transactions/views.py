from django.shortcuts import render
from django.db.models import Q
from .models import Transaction

def user_transactions(request):
    
    # Transactions initiated by the user
    user_transactions = Transaction.objects.filter(user=request.user)

    # Transactions involving the user's items
    user_items_transactions = Transaction.objects.filter(item__user=request.user)

    # Pass both sets of transactions to the template
    context = {
        'user_transactions': user_transactions,
        'user_items_transactions': user_items_transactions,
    }
    return render(request, 'user_transactions.html', context)
