from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomUserChangeForm, CustomAuthenticationForm
from .models import CustomUser


def customer_register(request):
    if request.user.is_authenticated:
        return redirect('chef:home')
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.role = 'customer'
                user.save()
                messages.success(request, f'Account created successfully! Welcome {user.username}!')
                login(request, user)
                return redirect('chef:home')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'customers/register.html', {'form': form, 'role': 'customer'})


def customer_login(request):
    if request.user.is_authenticated:
        return redirect('chef:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Role-based redirection
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                if user.role == 'admin' or user.is_superuser:
                    return redirect('management:dashboard')
                elif user.role == 'chef':
                    return redirect('chef:dashboard')
                else:
                    return redirect('chef:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'customers/login.html', {'form': form})


@login_required
def customer_profile(request):

    updated = False
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                updated = True
                messages.success(request, 'Profile updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'customers/profile.html', {
        'form': form,
        'updated': updated,
        'user_profile': request.user,
    })
