from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import time
from customers.models import CustomUser
from orders.models import Order
from .models import FoodItem, ChefProfile
from .forms import FoodItemForm


def get_current_category():
    """Get current meal category based on IST timezone"""
    ist = ZoneInfo('Asia/Kolkata')
    now = timezone.now().astimezone(ist).time()
    
    if time(18, 30) <= now or now < time(3, 0):
        return 'Dinner', 'Dinner Time (6:30 PM - 3:00 AM)'
    elif time(6, 0) <= now < time(12, 0):
        return 'Breakfast', 'Breakfast Time (6:00 AM - 12:00 PM)'
    elif time(12, 0) <= now < time(15, 30):
        return 'Lunch', 'Lunch Time (12:00 PM - 3:30 PM)'
    elif time(15, 30) <= now < time(18, 30):
        return 'Snacks', 'Snacks Time (3:30 PM - 6:30 PM)'
    else:
        return None, 'Kitchen Closed (3:00 AM - 6:00 AM)'


def food_list(request):
    """Display food items — filtered by selected category tab (default = current time)"""
    auto_category, time_message = get_current_category()

    # Allow the user to override the category via GET param
    selected = request.GET.get('category', auto_category or 'All')
    if selected not in ('All', 'Breakfast', 'Lunch', 'Snacks', 'Dinner'):
        selected = auto_category or 'All'

    if selected == 'All':
        foods = FoodItem.objects.filter(is_available=True).order_by('category', 'name')
    else:
        foods = FoodItem.objects.filter(is_available=True, category=selected)

    all_categories = ['All', 'Breakfast', 'Lunch', 'Snacks', 'Dinner']
    is_admin = request.user.is_authenticated and (
        request.user.is_superuser or request.user.role == 'admin'
    )

    return render(request, 'chef/food_list.html', {
        'foods': foods,
        'time_message': time_message,
        'current_category': auto_category,   # actual time-based category
        'selected_category': selected,        # what's currently displayed
        'all_categories': all_categories,
        'is_admin': is_admin,
    })


def food_detail(request, pk):
    """Display food item details"""
    food = get_object_or_404(FoodItem, pk=pk)
    return render(request, 'chef/food_detail.html', {'food': food})


def is_chef(user):
    return user.is_authenticated and (user.role == 'chef' or user.is_seller)


@login_required
def chef_dashboard(request):
    if not is_chef(request.user):
        messages.error(request, 'Access denied. Only chefs can access this.')
        return redirect('chef:home')
    
    food_items = FoodItem.objects.filter(chef=request.user)
    try:
        chef_profile = ChefProfile.objects.get(chef=request.user)
    except ChefProfile.DoesNotExist:
        chef_profile = ChefProfile.objects.create(chef=request.user)
    
    orders = Order.objects.filter(items__food_item__chef=request.user).distinct().order_by('-created_at')
    recent_orders = orders[:5]
    
    context = {
        'total_items': food_items.count(),
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='Pending').count(),
    }
    return render(request, 'chef/dashboard.html', context)


@login_required
def chef_menu(request):
    if not is_chef(request.user):
        messages.error(request, 'Access denied. Only chefs can access this.')
        return redirect('chef:home')
    
    food_items = FoodItem.objects.filter(chef=request.user)
    context = {
        'food_items': food_items,
    }
    return render(request, 'chef/chef_menu.html', context)


@login_required
def add_food(request):
    if not is_chef(request.user):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                food = form.save(commit=False)
                food.chef = request.user
                food.save()
                messages.success(request, f'{food.name} added successfully!')
                return redirect('chef:dashboard')
            except Exception as e:
                messages.error(request, f'Error adding food: {str(e)}')
    else:
        form = FoodItemForm()
    
    return render(request, 'chef/food_form.html', {'form': form, 'title': 'Add Food Item'})


@login_required
def edit_food(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    
    if food.chef != request.user:
        messages.error(request, 'You can only edit your own items.')
        return redirect('chef:dashboard')
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'{food.name} updated successfully!')
                return redirect('chef:dashboard')
            except Exception as e:
                messages.error(request, f'Error updating food: {str(e)}')
    else:
        form = FoodItemForm(instance=food)
    
    return render(request, 'chef/food_form.html', {'form': form, 'title': 'Edit Food Item'})


@login_required
def delete_food(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    
    if food.chef != request.user:
        messages.error(request, 'You can only delete your own items.')
        return redirect('chef:dashboard')
    
    if request.method == 'POST':
        name = food.name
        food.delete()
        messages.success(request, f'{name} deleted successfully!')
        return redirect('chef:dashboard')
    
    return render(request, 'chef/food_confirm_delete.html', {'food': food})
