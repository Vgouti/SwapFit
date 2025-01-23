from django.db import models
from django.contrib.auth.models import User

class WardrobeItem(models.Model):
    CATEGORY_CHOICES = [
        ('Tops', 'Tops'),
        ('Bottoms', 'Bottoms'),
        ('Dresses', 'Dresses'),
        ('Footwear', 'Footwear'),
        ('Accessories', 'Accessories'),
    ]

    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wardrobe_items')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='wardrobe_items/')
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Rent per day
    availability = models.BooleanField(default=True)  # Whether the item is available for rent/swap
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
