from django.urls import path
from .views import add_wardrobe_item, wardrobe_list, rent_items, request_swap, delete_wardrobe_item, manage_requests, approve_request, reject_request

urlpatterns = [
    path('add/', add_wardrobe_item, name='add_wardrobe_item'),
    path('', wardrobe_list, name='wardrobe_list'),
    path('delete/<int:item_id>/', delete_wardrobe_item, name='delete_wardrobe_item'),
    path('swap/<int:item_id>/', request_swap, name='request_swap'),
    path('rent-items/', rent_items, name='rent_items'),
    path('rent-items/<int:item_id>/', rent_items, name='rent_item_request'),
    path('manage_requests/', manage_requests, name='manage_requests'),
    path('approve_request/<int:transaction_id>/', approve_request, name='approve_request'),
    path('reject_request/<int:transaction_id>/', reject_request, name='reject_request'),
]
