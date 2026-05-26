from django.urls import path
from . import views

urlpatterns = [

    # Auth
    path('auth/send-otp/',    views.send_otp,    name='send_otp'),
    path('auth/verify-otp/',  views.verify_otp,  name='verify_otp'),

    # Products 
    path('products/',               views.product_list,         name='product_list'),
    path('products/most-bought/',   views.most_bought_products, name='most_bought'),
    path('products/<int:pk>/',      views.product_detail,       name='product_detail'),

    # Cart
    path('cart/add/',                    views.cart_add,    name='cart_add'),
    path('cart/update/<int:cart_id>/',   views.cart_update, name='cart_update'),
    path('cart/remove/<int:cart_id>/',   views.cart_remove, name='cart_remove'),
    path('cart/<int:user_id>/',          views.cart_list,   name='cart_list'),

    # Orders  
    path('orders/create/',               views.order_create, name='order_create'),
    path('orders/detail/<int:order_id>/',views.order_detail, name='order_detail'),
    path('orders/cancel/<int:order_id>/',views.order_cancel, name='order_cancel'),
    path('orders/<int:user_id>/',        views.order_list,   name='order_list'),
    # Wishlist
    path('wishlist/<int:user_id>/',          views.wishlist_list,   name='wishlist_list'),
    path('wishlist/add/',                    views.wishlist_add,    name='wishlist_add'),
    path('wishlist/remove/<int:wishlist_id>/',views.wishlist_remove, name='wishlist_remove'),

    # Reviews
    path('reviews/<int:product_id>/',        views.review_list,    name='review_list'),
    path('reviews/create/',                  views.review_create,  name='review_create'),
    path('reviews/delete/<int:review_id>/',  views.review_delete,  name='review_delete'),
    path('reviews/rating/<int:product_id>/', views.product_rating, name='product_rating'),
    path('seed/', views.seed_products, name='seed_products'),
]