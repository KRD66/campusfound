from django import forms
from .models import Item, Review


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_type', 'title', 'category', 'location', 'photo',
            'description', 'date_lost', 'reward_offered',
            'verification_question', 'phone_number', 'email'
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

            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': '+234 801 234 5678 (for WhatsApp)'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none',
                'placeholder': 'your.email@university.edu'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get('item_type')

        if item_type == 'found' and not cleaned_data.get('verification_question'):
            self.add_error('verification_question', 'Please add a verification question for found items')

        if item_type == 'lost' and not cleaned_data.get('date_lost'):
            self.add_error('date_lost', 'Please specify when you lost this item')
        
        # At least one contact method required
        if not cleaned_data.get('phone_number') and not cleaned_data.get('email'):
            raise forms.ValidationError('Please provide at least one contact method (phone or email)')

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