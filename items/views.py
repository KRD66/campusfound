from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import ItemForm, ReviewForm
from .models import Item, Review


def home(request):
    """Display all items with filtering and search"""
    item_type = request.GET.get('type', 'all')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'newest')
    
    items = Item.objects.all()
    
    if item_type in ['lost', 'found']:
        items = items.filter(item_type=item_type)
    
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    if sort_by == 'oldest':
        items = items.order_by('created_at')
    else:
        items = items.order_by('-created_at')
    
    return render(request, 'home.html', {
        'title': 'CampusFound | Lost & Found for Students',
        'items': items,
        'current_filter': item_type,
        'search_query': search_query,
        'current_sort': sort_by,
    })


def item_detail(request, item_id):
    """Display a single item's details"""
    item = get_object_or_404(Item, id=item_id)
    review_form = ReviewForm()
    
    # Check if user has already reviewed
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(item=item, reviewer=request.user).exists()
    
    return render(request, 'item_detail.html', {
        'item': item,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
    })


@login_required
def post_item(request):
    """Post a new item"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.poster = request.user
                item.save()
                messages.success(request, 'Item posted successfully!')
                return redirect('items:item_detail', item_id=item.id)
            except Exception as e:
                # Print the actual error
                print(f"Error saving item: {str(e)}")
                messages.error(request, f'Error posting item: {str(e)}')
                return render(request, 'post_item.html', {'form': form})
        else:
            # Print form errors
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ItemForm()

    return render(request, 'post_item.html', {'form': form})


@login_required
def dashboard(request):
    """User's personal dashboard"""
    filter_type = request.GET.get('filter', 'all')
    
    my_items = Item.objects.filter(poster=request.user)
    
    if filter_type in ['lost', 'found']:
        my_items = my_items.filter(item_type=filter_type)
    
    total_items = Item.objects.filter(poster=request.user).count()
    returned_items = Item.objects.filter(poster=request.user, status='returned').count()
    active_chats = 0  # No chat system anymore
    
    context = {
        'my_items': my_items,
        'total_items': total_items,
        'returned_items': returned_items,
        'active_chats': active_chats,
        'current_filter': filter_type,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def edit_item(request, item_id):
    """Edit an existing item"""
    item = get_object_or_404(Item, id=item_id, poster=request.user)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Item updated successfully!')
                return redirect('items:dashboard')
            except Exception as e:
                print(f"Error updating item: {str(e)}")
                messages.error(request, f'Error updating item: {str(e)}')
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'post_item.html', {'form': form, 'edit_mode': True})


@login_required
def delete_item(request, item_id):
    """Delete an item"""
    item = get_object_or_404(Item, id=item_id, poster=request.user)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('items:dashboard')
    
    return redirect('items:dashboard')


@login_required
def mark_as_returned(request, item_id):
    """Mark an item as returned"""
    item = get_object_or_404(Item, id=item_id, poster=request.user)
    
    if request.method == 'POST':
        item.status = 'returned'
        item.save()
        messages.success(request, 'Item marked as returned!')
    
    return redirect('items:dashboard')


@login_required
def claim_item(request, item_id):
    """Claim an item"""
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        if item.poster == request.user:
            messages.error(request, "You can't claim your own item!")
        elif item.status != 'active':
            messages.error(request, 'This item has already been claimed.')
        else:
            item.status = 'claimed'
            item.claimed_by = request.user
            item.save()
            messages.success(request, 'Item claimed! Please contact the poster to arrange pickup.')
            return redirect('items:item_detail', item_id=item.id)
    
    return redirect('items:item_detail', item_id=item.id)


@login_required
def add_review(request, item_id):
    """Add a review for a returned item"""
    item = get_object_or_404(Item, id=item_id)
    
    # Only the person who claimed the item can leave a review
    if request.user != item.claimed_by:
        messages.error(request, 'Only the person who claimed this item can leave a review.')
        return redirect('items:item_detail', item_id=item.id)
    
    # Item must be returned
    if item.status != 'returned':
        messages.error(request, 'You can only review items that have been returned.')
        return redirect('items:item_detail', item_id=item.id)
    
    # Check if user already reviewed
    if Review.objects.filter(item=item, reviewer=request.user).exists():
        messages.error(request, 'You have already reviewed this item.')
        return redirect('items:item_detail', item_id=item.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Review posted successfully!')
            return redirect('items:item_detail', item_id=item.id)
    
    return redirect('items:item_detail', item_id=item.id)