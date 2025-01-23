from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WardrobeItem
from transactions.models import Transaction
from datetime import datetime
@login_required
def add_wardrobe_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        color = request.POST.get('color')
        size = request.POST.get('size')
        price_per_day = request.POST.get('price_per_day')
        availability = request.POST.get('availability')

        # Validation (optional, expand as needed)
        if not name or not category or not image:
            messages.error(request, 'Name, category, and image are required.')
            return redirect('add_wardrobe_item')

        # Save the wardrobe item
        WardrobeItem.objects.create(
            user=request.user,
            name=name,
            category=category,
            image=image,
            description=description,
            color=color,
            size=size,
            price_per_day=price_per_day,
            availability=availability == 'on'  # Convert checkbox value to boolean
        )
        messages.success(request, 'Wardrobe item added successfully!')
        return redirect('wardrobe_list')

    return render(request, 'add_wardrobe_item.html')

def wardrobe_list(request):
    wardrobe_items = WardrobeItem.objects.filter(user=request.user).order_by('-added_on')
    return render(request, 'profile.html', {'wardrobe_items': wardrobe_items})

def delete_wardrobe_item(request, item_id):
    item = get_object_or_404(WardrobeItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Wardrobe item deleted successfully!")
    return redirect('profile')

@login_required
def request_swap(request, item_id):
    item_requested = get_object_or_404(WardrobeItem, id=item_id)
    user_items = WardrobeItem.objects.filter(user=request.user, availability=True)

    if item_requested.user == request.user:
        messages.error(request, "You cannot swap with your own item.")
        return redirect('wardrobe_list')

    if request.method == 'POST':
        offered_item_id = request.POST.get('offered_item')
        item_offered = get_object_or_404(WardrobeItem, id=offered_item_id, user=request.user)

        # Create transaction for swap
        Transaction.objects.create(
            user=request.user,
            item=item_requested,
            transaction_type='Swap',
            counterparty=item_requested.user,
            offered_item=item_offered,  # Assuming you track offered item in the transaction model
            status='Pending',
        )

        # Mark both items as unavailable
        item_requested.availability = False
        item_offered.availability = False
        item_requested.save()
        item_offered.save()

        messages.success(request, f"Swap request for {item_requested.name} has been sent.")
        return redirect('wardrobe_list')

    return render(request, 'request_swap.html', {'item_requested': item_requested, 'user_items': user_items})
@login_required
def rent_items(request, item_id=None):
    if request.method == "GET":
        # Display all items available for rent
        items = WardrobeItem.objects.filter(availability=True).exclude(user=request.user)
        return render(request, 'rent_item.html', {'items': items})

    elif request.method == "POST" and item_id:
        # Handle rent request
        item = get_object_or_404(WardrobeItem, id=item_id)

        if item.user == request.user:
            messages.error(request, "You cannot rent your own item.")
            return redirect('rent_items')

        # Get rental details from the form
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not start_date or not end_date:
            messages.error(request, "Please provide valid start and end dates.")
            return redirect('rent_items')

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        if end_date <= start_date:
            messages.error(request, "End date must be after start date.")
            return redirect('rent_items')

        # Calculate rental fee
        rental_days = (end_date - start_date).days
        rental_fee = item.price_per_day * rental_days

        # Create a pending rent transaction
        Transaction.objects.create(
            user=request.user,
            item=item,
            transaction_type='Rent',
            counterparty=item.user,
            amount=rental_fee,
            start_date=start_date,
            end_date=end_date,
            status='Pending',
        )

        messages.success(request, f"Rent request for {item.name} sent for approval.")
        return redirect('rent_items')


@login_required
def manage_requests(request):
    pending_requests = Transaction.objects.filter(counterparty=request.user, status='Pending')
    return render(request, 'manage_requests.html', {'pending_requests': pending_requests})

@login_required
def approve_request(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, counterparty=request.user)
    transaction.status = 'Approved'
    transaction.item.availability = False
    transaction.item.save()
    transaction.save()

    messages.success(request, "The request has been approved.")
    return redirect('manage_requests')

@login_required
def reject_request(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, counterparty=request.user)
    transaction.status = 'Rejected'
    transaction.save()

    messages.success(request, "The request has been rejected.")
    return redirect('manage_requests')
