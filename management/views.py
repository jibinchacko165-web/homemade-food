from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from customers.models import CustomUser
from chef.models import FoodItem, ChefProfile
from orders.models import Order


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'admin')


@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied. Admin only.')
        return redirect('home')
    
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_chefs': CustomUser.objects.filter(role='chef').count(),
        'total_customers': CustomUser.objects.filter(role='customer').count(),
        'total_food_items': FoodItem.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='Pending').count(),
        'completed_orders': Order.objects.filter(status='Completed').count(),
    }
    
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    recent_users = CustomUser.objects.all().order_by('-date_joined')[:10]
    
    context = {
        'stats': stats,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def manage_users(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    users = CustomUser.objects.all()
    role_filter = request.GET.get('role')
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'roles': ['customer', 'chef', 'admin'],
        'current_filter': role_filter,
    }
    return render(request, 'admin/manage_users.html', context)


@login_required
def manage_food_items(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    foods = FoodItem.objects.all()
    context = {'foods': foods}
    return render(request, 'admin/manage_food_items.html', context)


@login_required
def manage_orders(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    orders = Order.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'statuses': ['Pending', 'Completed', 'Cancelled'],
        'current_filter': status_filter,
    }
    return render(request, 'admin/manage_orders.html', context)


@login_required
def toggle_user_status(request, user_id):
    if not is_admin(request.user):
        return redirect('home')
    
    user = CustomUser.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f'User {user.username} {status}!')
    return redirect('admin:manage_users')


@login_required
def toggle_food_availability(request, food_id):
    if not is_admin(request.user):
        return redirect('home')
    
    food = FoodItem.objects.get(id=food_id)
    food.is_available = not food.is_available
    food.save()
    
    status = "available" if food.is_available else "unavailable"
    messages.success(request, f'{food.name} marked as {status}!')
    return redirect('admin:manage_food_items')
