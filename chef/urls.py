from django.urls import path
from . import views

app_name = 'chef'

urlpatterns = [
    # Food listing (public)
    path('', views.food_list, name='home'),
    path('food/<int:pk>/', views.food_detail, name='food_detail'),
    
    path('dashboard/', views.chef_dashboard, name='dashboard'),
    path('menu/', views.chef_menu, name='menu'),
    path('food/add/', views.add_food, name='add_food'),
    path('food/<int:pk>/edit/', views.edit_food, name='edit_food'),
    path('food/<int:pk>/delete/', views.delete_food, name='delete_food'),
]
