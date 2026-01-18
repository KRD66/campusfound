from django.db.models import Q
from .models import Message, Conversation


def unread_messages(request):
    """
    Add unread message count to all templates
    """
    if request.user.is_authenticated:
        # Get all conversations where user is involved
        conversations = Conversation.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        )
        
        # Count unread messages (not sent by current user)
        unread_count = Message.objects.filter(
            conversation__in=conversations,
            is_read=False
        ).exclude(sender=request.user).count()
        
        return {'unread_messages_count': unread_count}
    
    return {'unread_messages_count': 0}