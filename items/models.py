from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from cloudinary.models import CloudinaryField

User = get_user_model()


class Item(models.Model):
    TYPE_CHOICES = (
        ('found', 'Found'),
        ('lost', 'Lost'),
    )

    CATEGORY_CHOICES = (
        ('Electronics', 'Electronics'),
        ('Keys', 'Keys'),
        ('Books', 'Books'),
        ('Clothing', 'Clothing'),
        ('ID/Cards', 'ID/Cards'),
        ('Bags', 'Bags'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('claimed', 'Claimed'),
        ('returned', 'Returned'),
    )

    # Common fields
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        help_text="Select a category"
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Type the location (e.g. Main Library, Science Cafe...)"
    )
    
    # Cloudinary image
    photo = CloudinaryField(
        'image',
        blank=True,
        null=True,
        resource_type='image',
        folder='campusfound/items',
        help_text="Upload photo of the item"
    )
    
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Lost-item-specific
    date_lost = models.DateField(
        blank=True,
        null=True,
        help_text="When did you lose this item?"
    )
    reward_offered = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional: e.g. '$20 reward' or 'Coffee on me!'"
    )

    # Found-item-specific
    verification_question = models.TextField(
        blank=True,
        help_text="Ask a question only the owner would know"
    )

    # Contact fields (replaces chat system)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Your phone/WhatsApp number (e.g. +2348012345678)"
    )
    email = models.EmailField(
        max_length=200,
        blank=True,
        help_text="Your email address"
    )

    # Status and claimer
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    claimed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='claimed_items',
        help_text="User who claimed this item"
    )

    def __str__(self):
        return f"{self.item_type.title()}: {self.title}"

    def get_whatsapp_link(self):
        """Generate WhatsApp link from phone number"""
        if self.phone_number:
            # Remove spaces, dashes, and other non-numeric characters
            clean_number = ''.join(filter(str.isdigit, self.phone_number))
            # Add + if not present
            if not clean_number.startswith('+'):
                clean_number = '+' + clean_number
            return f"https://wa.me/{clean_number}"
        return None

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    """Reviews for returned items"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    comment = models.TextField(help_text="Share your experience")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Ensure one review per user per item
        unique_together = ['item', 'reviewer']

    def __str__(self):
        return f"Review by {self.reviewer.email} for {self.item.title}"