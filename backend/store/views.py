import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import User, Product, Cart, Order, Wishlist, Review
from .serializers import (
    UserSerializer, ProductSerializer,
    CartSerializer, OrderSerializer,
    WishlistSerializer, ReviewSerializer
)
 
 
# Auth
 
@api_view(['POST'])
def send_otp(request):
    """Send OTP to a mobile number (simulated)."""
    mobile = request.data.get('mobile')
    if not mobile:
        return Response({'error': 'Mobile number required'}, status=400)
 
    otp = str(random.randint(100000, 999999))
    user, created = User.objects.get_or_create(mobile=mobile)
    user.otp = otp
    user.save()
 
    return Response({'message': 'OTP sent', 'otp': otp, 'created': created})
 
 
@api_view(['POST'])
def verify_otp(request):
    """Verify OTP and return user details."""
    mobile = request.data.get('mobile')
    otp = request.data.get('otp')
    full_name = request.data.get('full_name', '')
 
    try:
        user = User.objects.get(mobile=mobile)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
 
    if user.otp != otp:
        return Response({'error': 'Invalid OTP'}, status=400)
 
    if full_name:
        user.full_name = full_name
    user.otp = None
    user.save()
 
    return Response({'message': 'Login successful', 'user': UserSerializer(user).data})
 
 
# Products
 
@api_view(['GET'])
def product_list(request):
    """
    Fetch all products.
    Optional query params:
      ?category=Electronics
      ?sold=true
      ?is_sale=true
      ?min_price=100&max_price=500
      ?search=headphones
    """
    products = Product.objects.all()
 
    category = request.query_params.get('category')
    sold = request.query_params.get('sold')
    is_sale = request.query_params.get('is_sale')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    search = request.query_params.get('search')
 
    if category:
        products = products.filter(category__iexact=category)
    if sold is not None:
        products = products.filter(sold=(sold.lower() == 'true'))
    if is_sale is not None:
        products = products.filter(is_sale=(is_sale.lower() == 'true'))
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    if search:
        products = products.filter(title__icontains=search)
 
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
 
 
@api_view(['GET'])
def product_detail(request, pk):
    """Get a single product by ID."""
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    return Response(ProductSerializer(product).data)
 
 
@api_view(['GET'])
def most_bought_products(request):
    """Return top 5 products by total order quantity."""
    top = (
        Order.objects
        .filter(is_cancelled=False)
        .values('product')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )
    product_ids = [item['product'] for item in top]
    products = Product.objects.filter(id__in=product_ids)
    return Response(ProductSerializer(products, many=True).data)
 
 
# Cart
 
@api_view(['GET'])
def cart_list(request, user_id):
    """Get all cart items for a user."""
    items = Cart.objects.filter(user_id=user_id).select_related('product')
    return Response(CartSerializer(items, many=True).data)
 
 
@api_view(['POST'])
def cart_add(request):
    """
    Add a product to cart.
    Body: { user_id, product_id, quantity }
    """
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
 
    try:
        user = User.objects.get(pk=user_id)
        product = Product.objects.get(pk=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return Response({'error': 'User or Product not found'}, status=404)
 
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
 
    return Response(CartSerializer(cart_item).data, status=201)
 
 
@api_view(['PATCH'])
def cart_update(request, cart_id):
    """
    Increase or decrease quantity.
    Body: { action: 'increase' | 'decrease' }
    """
    try:
        item = Cart.objects.get(pk=cart_id)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)
 
    action = request.data.get('action')
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            return Response({'message': 'Item removed from cart'})
 
    return Response(CartSerializer(item).data)
 
 
@api_view(['DELETE'])
def cart_remove(request, cart_id):
    """Remove a product from cart."""
    try:
        item = Cart.objects.get(pk=cart_id)
        item.delete()
        return Response({'message': 'Removed from cart'})
    except Cart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)
 
 
# Orders
 
@api_view(['POST'])
def order_create(request):
    """
    Place an order.
    Body: { user_id, product_id, quantity, payment_mode }
    """
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    payment_mode = request.data.get('payment_mode', 'COD')
 
    try:
        user = User.objects.get(pk=user_id)
        product = Product.objects.get(pk=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return Response({'error': 'User or Product not found'}, status=404)
 
    order = Order.objects.create(
        user=user,
        product=product,
        price=product.price,
        quantity=quantity,
        payment_mode=payment_mode,
    )
    return Response(OrderSerializer(order).data, status=201)
 
 
@api_view(['GET'])
def order_list(request, user_id):
    """Get all orders for a user."""
    orders = Order.objects.filter(user_id=user_id).select_related('product')
    return Response(OrderSerializer(orders, many=True).data)
 
 
@api_view(['GET'])
def order_detail(request, order_id):
    """Get details of a single order."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    return Response(OrderSerializer(order).data)
 
 
@api_view(['PATCH'])
def order_cancel(request, order_id):
    """Cancel an order."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
 
    if order.is_cancelled:
        return Response({'error': 'Order already cancelled'}, status=400)
 
    order.is_cancelled = True
    order.save()
    return Response({'message': 'Order cancelled', 'order': OrderSerializer(order).data})
 
 
# Wishlist
 
@api_view(['GET'])
def wishlist_list(request, user_id):
    """Get all wishlist items for a user."""
    items = Wishlist.objects.filter(user_id=user_id).select_related('product')
    return Response(WishlistSerializer(items, many=True).data)
 
 
@api_view(['POST'])
def wishlist_add(request):
    """
    Add product to wishlist.
    Body: { user_id, product_id }
    """
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')
 
    try:
        user = User.objects.get(pk=user_id)
        product = Product.objects.get(pk=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return Response({'error': 'User or Product not found'}, status=404)
 
    item, created = Wishlist.objects.get_or_create(user=user, product=product)
    if not created:
        return Response({'message': 'Already in wishlist'}, status=200)
    return Response(WishlistSerializer(item).data, status=201)
 
 
@api_view(['DELETE'])
def wishlist_remove(request, wishlist_id):
    """Remove item from wishlist."""
    try:
        item = Wishlist.objects.get(pk=wishlist_id)
        item.delete()
        return Response({'message': 'Removed from wishlist'})
    except Wishlist.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)
 
 
# Reviews
 
@api_view(['GET'])
def review_list(request, product_id):
    """Get all reviews for a product."""
    reviews = Review.objects.filter(product_id=product_id).select_related('user')
    return Response(ReviewSerializer(reviews, many=True).data)
 
 
@api_view(['POST'])
def review_create(request):
    """
    Create or update a review.
    Body: { user_id, product_id, rating, comment }
    """
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')
    rating = int(request.data.get('rating', 5))
    comment = request.data.get('comment', '')
 
    if rating < 1 or rating > 5:
        return Response({'error': 'Rating must be between 1 and 5'}, status=400)
 
    try:
        user = User.objects.get(pk=user_id)
        product = Product.objects.get(pk=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return Response({'error': 'User or Product not found'}, status=404)
 
    review, created = Review.objects.update_or_create(
        user=user, product=product,
        defaults={'rating': rating, 'comment': comment}
    )
    return Response(ReviewSerializer(review).data, status=201 if created else 200)
 
 
@api_view(['DELETE'])
def review_delete(request, review_id):
    """Delete a review."""
    try:
        review = Review.objects.get(pk=review_id)
        review.delete()
        return Response({'message': 'Review deleted'})
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=404)
 
 
@api_view(['GET'])
def product_rating(request, product_id):
    """Get average rating and count for a product."""
    from django.db.models import Avg, Count
    result = Review.objects.filter(product_id=product_id).aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    return Response({
        'product_id': product_id,
        'avg_rating': round(result['avg_rating'] or 0, 1),
        'total_reviews': result['total_reviews']
    })
 
 
@api_view(['GET'])
def seed_products(request):
    """Visit this URL once to seed the database."""
    products = [
        {"title": "Wireless Headphones", "price": 150.0, "description": "High-quality wireless headphones with noise cancellation.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "sold": False, "is_sale": True},
        {"title": "Gaming Laptop", "price": 1200.0, "description": "High-performance laptop for gaming and productivity.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400", "sold": False, "is_sale": False},
        {"title": "Running Shoes", "price": 85.0, "description": "Lightweight running shoes for everyday training.", "category": "Sports", "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "sold": False, "is_sale": True},
        {"title": "Coffee Maker", "price": 60.0, "description": "Automatic drip coffee maker with 12-cup capacity.", "category": "Kitchen", "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400", "sold": False, "is_sale": False},
        {"title": "Yoga Mat", "price": 35.0, "description": "Non-slip yoga mat with carrying strap.", "category": "Sports", "image_url": "https://images.unsplash.com/photo-1601925228008-4bb42b1e0a3b?w=400", "sold": False, "is_sale": False},
        {"title": "Smartwatch", "price": 250.0, "description": "Feature-packed smartwatch with health tracking.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", "sold": False, "is_sale": True},
        {"title": "Backpack", "price": 70.0, "description": "Durable 30L backpack for travel and hiking.", "category": "Travel", "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "sold": False, "is_sale": False},
        {"title": "Desk Lamp", "price": 45.0, "description": "LED desk lamp with adjustable brightness.", "category": "Home", "image_url": "https://images.unsplash.com/photo-1543198126-a8ad8e47fb22?w=400", "sold": False, "is_sale": False},
        {"title": "Bluetooth Speaker", "price": 90.0, "description": "Portable waterproof Bluetooth speaker.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "sold": False, "is_sale": True},
        {"title": "Cookware Set", "price": 120.0, "description": "10-piece non-stick cookware set.", "category": "Kitchen", "image_url": "https://images.unsplash.com/photo-1584990347449-39e171f89765?w=400", "sold": False, "is_sale": False},
        {"title": "Sunglasses", "price": 55.0, "description": "UV400 polarized sunglasses.", "category": "Fashion", "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400", "sold": False, "is_sale": True},
        {"title": "Mechanical Keyboard", "price": 110.0, "description": "Tactile mechanical keyboard with RGB backlighting.", "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400", "sold": False, "is_sale": False},
    ]
 
    if Product.objects.exists():
        return Response({
            'message': 'Database already has products.',
            'count': Product.objects.count()
        })
 
    for p in products:
        Product.objects.create(**p)
 
    return Response({
        'message': f'Successfully seeded {len(products)} products!',
        'count': Product.objects.count()
    })