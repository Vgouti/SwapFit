from django.db import models
from django.contrib.auth.models import User
from wardrobe.models import WardrobeItem

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Swap', 'Swap'),
        ('Rent', 'Rent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    item = models.ForeignKey(WardrobeItem, on_delete=models.CASCADE)
    offered_item = models.ForeignKey(WardrobeItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='offered_transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    counterparty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counter_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} by {self.user.username} for {self.item.name}"
