from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('items:home')
    
    if request.method == 'POST':
        email = request.POST.get('username')  # Using 'username' field name from form
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to 'next' parameter if exists, otherwise go to home
            next_url = request.GET.get('next', 'items:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('items:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name', '')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
        else:
            # Create user
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                full_name=full_name
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('items:home')
    
    return render(request, 'accounts/register.html')