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
            return redirect('items:home')  # or to dashboard later
    else:
        form = ItemForm()

    return render(request, 'post_item.html', {'form': form})