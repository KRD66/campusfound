from django.db import models
from django.contrib.auth import get_user_model
from items.models import Item

User = get_user_model()


class Conversation(models.Model):
    """
    A conversation between two users about a specific item
    """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='conversations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_conversations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = ['item', 'sender', 'receiver']
    
    def __str__(self):
        return f"Conversation about {self.item.title} between {self.sender.email} and {self.receiver.email}"
    
    def get_other_user(self, user):
        """Get the other user in the conversation"""
        return self.receiver if user == self.sender else self.sender
    
    def get_last_message(self):
        """Get the last message in this conversation"""
        return self.messages.first()


class Message(models.Model):
    """
    Individual message in a conversation
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"