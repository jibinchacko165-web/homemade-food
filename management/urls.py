from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('food-items/', views.manage_food_items, name='manage_food_items'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('food/<int:food_id>/toggle-availability/', views.toggle_food_availability, name='toggle_food_availability'),
]
