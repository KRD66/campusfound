from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.contrib import messages as django_messages
from .models import Conversation, Message
from items.models import Item


@login_required
def inbox(request):
    """Display all conversations for the logged-in user"""
    # Get all conversations where user is either sender or receiver
    conversations = Conversation.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('item', 'sender', 'receiver').prefetch_related('messages')
    
    # Get unread count
    unread_count = Message.objects.filter(
        conversation__in=conversations,
        is_read=False
    ).exclude(sender=request.user).count()
    
    context = {
        'conversations': conversations,
        'unread_count': unread_count,
    }
    
    return render(request, 'messages/inbox.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Display a specific conversation and handle sending messages"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id
    )
    
    # Check if user is part of this conversation
    if request.user not in [conversation.sender, conversation.receiver]:
        django_messages.error(request, "You don't have access to this conversation")
        return redirect('messages:inbox')
    
    # Mark messages as read
    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    # Handle sending new message
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            return redirect('messages:conversation_detail', conversation_id=conversation.id)
    
    # Get all messages in this conversation
    messages_list = conversation.messages.all().order_by('created_at')
    
    # Get all conversations for sidebar
    all_conversations = Conversation.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('item', 'sender', 'receiver')
    
    context = {
        'conversation': conversation,
        'messages_list': messages_list,
        'all_conversations': all_conversations,
        'other_user': conversation.get_other_user(request.user),
    }
    
    return render(request, 'messages/conversation_detail.html', context)


@login_required
def start_conversation(request, item_id):
    """Start a new conversation about an item"""
    item = get_object_or_404(Item, id=item_id)
    
    # Can't message yourself
    if item.poster == request.user:
        django_messages.error(request, "You can't message yourself about your own item")
        return redirect('items:item_detail', item_id=item.id)
    
    # Check if conversation already exists
    conversation = Conversation.objects.filter(
        item=item,
        sender=request.user,
        receiver=item.poster
    ).first()
    
    if not conversation:
        # Check reverse (if item poster already messaged current user)
        conversation = Conversation.objects.filter(
            item=item,
            sender=item.poster,
            receiver=request.user
        ).first()
    
    # Create new conversation if doesn't exist
    if not conversation:
        conversation = Conversation.objects.create(
            item=item,
            sender=request.user,
            receiver=item.poster
        )
    
    return redirect('messages:conversation_detail', conversation_id=conversation.id)
