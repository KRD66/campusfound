from django import forms
from .models import Item, Review


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_type', 'title', 'category', 'location', 'photo',
            'description', 'date_lost', 'reward_offered',
            'verification_question', 'contact_info'
        ]

        widgets = {
            'item_type': forms.HiddenInput(),

            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'e.g. Silver MacBook Air'
            }),

            'category': forms.Select(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 outline-none'
            }),

            'location': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'e.g. Main Library, Science Cafe, Student Union...'
            }),

            'photo': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'id_photo'
            }),

            'description': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 outline-none',
                'rows': 4,
                'placeholder': 'Describe the item in detail...'
            }),

            'date_lost': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none'
            }),

            'reward_offered': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'e.g. $20 reward, Coffee on me! (optional)'
            }),

            'verification_question': forms.Textarea(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 outline-none',
                'rows': 3,
                'placeholder': 'e.g. What stickers are on the laptop? What color is the case?'
            }),

            'contact_info': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'Email or Phone Number (e.g. email@example.com or 08012345678)'
            }),
        }

    def clean_contact_info(self):
        """Auto-detect and format phone numbers as WhatsApp links"""
        contact = self.cleaned_data.get('contact_info', '').strip()
        
        if contact:
            # Check if it's an email (contains @)
            if '@' in contact:
                return contact
            
            # Otherwise treat as phone number
            # Remove any spaces, dashes, or parentheses
            phone = contact.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            
            # If it doesn't already have whatsapp: prefix, add it
            if not phone.startswith('whatsapp:'):
                # Add + if not present and starts with country code
                if not phone.startswith('+'):
                    # Assume Nigerian number if starts with 0
                    if phone.startswith('0'):
                        phone = '+234' + phone[1:]
                    else:
                        phone = '+' + phone
                
                return f'whatsapp:{phone}'
            
            return phone
        
        return contact

    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get('item_type')

        if item_type == 'found' and not cleaned_data.get('verification_question'):
            self.add_error('verification_question', 'Please add a verification question for found items')

        if item_type == 'lost' and not cleaned_data.get('date_lost'):
            self.add_error('date_lost', 'Please specify when you lost this item')

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'hidden'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full p-4 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none',
                'rows': 4,
                'placeholder': 'Share your experience with this exchange...'
            }),
        }
        labels = {
            'rating': 'Rating',
            'comment': 'Your Review'
        }