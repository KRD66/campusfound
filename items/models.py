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

    CONTACT_PREFERENCE_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('chat', 'In-App Chat'),
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
    contact_preference = models.CharField(
        max_length=20,
        choices=CONTACT_PREFERENCE_CHOICES,
        default='chat',
        blank=True
    )

    # Found-item-specific
    verification_question = models.TextField(
        blank=True,
        help_text="Ask a question only the owner would know"
    )

    # New contact field
    contact_info = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional: your email or WhatsApp number (e.g. whatsapp:+2348012345678)"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return f"{self.item_type.title()}: {self.title}"

    class Meta:
        ordering = ['-created_at']