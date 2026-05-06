from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from customers.models import CustomUser
from chef.models import FoodItem, ChefProfile
from orders.models import Order, OrderItem
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import json
from .forms import StaffCreationForm


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'admin')


@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied. Admin only.')
        return redirect('chef:home')
    
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
    
    # Analytics: Total Revenue
    total_revenue = Order.objects.filter(status='Completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    stats['total_revenue'] = total_revenue

    # Analytics: Monthly Revenue Data for Chart (Computed in Python to avoid SQLite timezone errors)
    monthly_revenue = {}
    for order in Order.objects.filter(status='Completed'):
        sort_key = order.created_at.strftime('%Y-%m')
        label_key = order.created_at.strftime('%b %Y')
        
        if sort_key not in monthly_revenue:
            monthly_revenue[sort_key] = {'label': label_key, 'revenue': 0}
            
        monthly_revenue[sort_key]['revenue'] += float(order.total_price)
        
    # Sort chronologically
    sorted_keys = sorted(monthly_revenue.keys())
    
    months = [monthly_revenue[k]['label'] for k in sorted_keys]
    revenues = [monthly_revenue[k]['revenue'] for k in sorted_keys]

    # Analytics: Top Selling Dishes
    top_dishes = OrderItem.objects.filter(order__status='Completed') \
        .values('food_item__name', 'food_item__chef__username') \
        .annotate(total_sold=Sum('quantity'), revenue=Sum('price')) \
        .order_by('-total_sold')[:5]
    
    context = {
        'stats': stats,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'chart_months': json.dumps(months),
        'chart_revenues': json.dumps(revenues),
        'top_dishes': top_dishes,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def manage_users(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('chef:home')
    
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
        return redirect('chef:home')
    
    foods = FoodItem.objects.all()
    context = {'foods': foods}
    return render(request, 'admin/manage_food_items.html', context)


@login_required
def manage_orders(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('chef:home')
    
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
        return redirect('chef:home')
    
    user = CustomUser.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f'User {user.username} {status}!')
    return redirect('management:manage_users')


@login_required
def toggle_food_availability(request, food_id):
    if not is_admin(request.user):
        return redirect('chef:home')
    
    food = FoodItem.objects.get(id=food_id)
    food.is_available = not food.is_available
    food.save()
    
    status = "available" if food.is_available else "unavailable"
    messages.success(request, f'{food.name} marked as {status}!')
    return redirect('management:manage_food_items')
@login_required
def create_staff(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('chef:home')
    
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Staff member {user.username} created successfully as {user.get_role_display()}!')
            return redirect('management:manage_users')
    else:
        form = StaffCreationForm()
    
    return render(request, 'admin/create_staff.html', {'form': form})
