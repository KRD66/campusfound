from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ItemForm
from .models import Item


def home(request):
    # Get filter parameters from URL
    item_type = request.GET.get('type', 'all')  # 'all', 'lost', or 'found'
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'newest')  # 'newest' or 'oldest'
    
    # Start with all items
    items = Item.objects.all()
    
    # Filter by type
    if item_type in ['lost', 'found']:
        items = items.filter(item_type=item_type)
    
    # Search functionality
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Sorting
    if sort_by == 'oldest':
        items = items.order_by('created_at')
    else:  # newest (default)
        items = items.order_by('-created_at')
    
    return render(request, 'home.html', {
        'title': 'CampusFound | Lost & Found for Students',
        'items': items,
        'current_filter': item_type,
        'search_query': search_query,
        'current_sort': sort_by,
    })


def item_detail(request, item_id):
    """View for displaying a single item's details"""
    item = get_object_or_404(Item, id=item_id)
    
    return render(request, 'item_detail.html', {
        'item': item,
    })
    
    
@login_required
def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.poster = request.user
            item.save()
            return redirect('items:dashboard')
    else:
        form = ItemForm()

    return render(request, 'post_item.html', {'form': form})


@login_required
def dashboard(request):
    """User's personal dashboard showing their items"""
    from chats.models import Conversation
    from django.db.models import Q
    
    filter_type = request.GET.get('filter', 'all')
    
    # Get user's items
    my_items = Item.objects.filter(poster=request.user)
    
    # Apply filter
    if filter_type in ['lost', 'found']:
        my_items = my_items.filter(item_type=filter_type)
    
    # Calculate stats
    total_items = Item.objects.filter(poster=request.user).count()
    returned_items = Item.objects.filter(poster=request.user, status='returned').count()
    
    # Get active chats count
    active_chats = Conversation.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).count()
    
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
            form.save()
            return redirect('items:dashboard')
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'post_item.html', {'form': form, 'edit_mode': True})


@login_required
def delete_item(request, item_id):
    """Delete an item"""
    item = get_object_or_404(Item, id=item_id, poster=request.user)
    
    if request.method == 'POST':
        item.delete()
        return redirect('items:dashboard')
    
    return redirect('items:dashboard')


@login_required
def mark_as_returned(request, item_id):
    """Mark an item as returned"""
    item = get_object_or_404(Item, id=item_id, poster=request.user)
    
    if request.method == 'POST':
        item.status = 'returned'
        item.save()
    
    return redirect('items:dashboard')