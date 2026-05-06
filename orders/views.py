from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order, OrderItem
from chef.models import FoodItem

def is_seller(user):
    return user.is_authenticated and user.is_seller

@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id)
    cart = request.session.get('cart', {})
    if str(food_id) in cart:
        cart[str(food_id)]['quantity'] += 1
    else:
        cart[str(food_id)] = {'price': str(food.price), 'quantity': 1, 'name': food.name}
    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    items_to_remove = []
    
    for food_id, item in cart.items():
        try:
            food = FoodItem.objects.get(pk=food_id)
            total = float(item['price']) * item['quantity']
            total_price += total
            cart_items.append({
                'food': food,
                'quantity': item['quantity'],
                'total': total
            })
        except FoodItem.DoesNotExist:
            items_to_remove.append(food_id)
            
    # Clean up cart if items were deleted
    if items_to_remove:
        for food_id in items_to_remove:
            del cart[str(food_id)]
        request.session['cart'] = cart
        
    return render(request, 'orders/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, food_id):
    cart = request.session.get('cart', {})
    if str(food_id) in cart:
        del cart[str(food_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('home')
    
    # Recalculate total safely
    total_price = 0
    valid_items = []
    
    for food_id, item in cart.items():
        try:
            food = FoodItem.objects.get(pk=food_id)
            total_price += float(item['price']) * item['quantity']
            valid_items.append((food, item))
        except FoodItem.DoesNotExist:
            continue
            
    if not valid_items:
        request.session['cart'] = {}
        return redirect('home')
        
    order = Order.objects.create(customer=request.user, total_price=total_price)
    
    for food, item in valid_items:
        OrderItem.objects.create(
            order=order,
            food_item=food,
            quantity=item['quantity'],
            price=item['price']
        )
    
    # clear cart
    request.session['cart'] = {}
    return redirect('order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@user_passes_test(is_seller)
def seller_orders(request):
    # Sellers see orders containing their foods
    orders = Order.objects.filter(items__food_item__seller=request.user).distinct().order_by('-created_at')
    return render(request, 'orders/seller_orders.html', {'orders': orders})

@user_passes_test(is_seller)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
    return redirect('seller_orders')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    # Check permission
    if order.customer != request.user and not request.user.is_seller:
        return redirect('home')
    return render(request, 'orders/order_detail.html', {'order': order})
