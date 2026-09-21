from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .recommender import get_similar_products
import json

# FR-3: عرض المنتجات مع البحث والفلترة بالتصنيف
def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)
        
    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    })

# FR-3 & FR-6: تفاصيل المنتج + ترشيحات الذكاء الاصطناعي وتفسيرها
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    recommendations = get_similar_products(product.id)
    return render(request, 'store/product_detail.html', {
        'product': product,
        'recommendations': recommendations
    })

# FR-4: إضافة منتج إلى السلة عبر Vanilla JS (API Endpoint)
@login_required
def add_to_cart_api(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        total_items = sum(item.quantity for item in cart.items.all())
        return JsonResponse({'status': 'success', 'total_items': total_items})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# FR-4: عرض صفحة السلة
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'store/cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

# FR-5: تأكيد الطلب وعرض الـ History
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    if not items:
        return redirect('product_list')
        
    total_price = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(user=request.user, total_price=total_price, status='Pending')
    
    for item in items:
        OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
    
    items.delete()
    return redirect('order_history')

@login_required
def order_history(request):
    orders = request.user.orders.prefetch_related('items__product').order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

# FR-1: تسجيل مستخدم جديد وتسجيل الدخول
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('product_list')
