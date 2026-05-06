from django.urls import path
from . import views
app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('manage/', views.seller_orders, name='seller_orders'),
    path('manage/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('api/check-new-orders/', views.check_new_orders, name='check_new_orders'),
    path('api/check-order-status/', views.check_order_status, name='check_order_status'),
]
