from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'customers'

urlpatterns = [
    path('register/', views.customer_register, name='register'),
    path('login/', views.customer_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='customers/logout.html'), name='logout'),
    path('profile/', views.customer_profile, name='profile'),
]
