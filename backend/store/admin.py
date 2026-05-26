from django.contrib import admin
from .models import User, Product, Cart, Order, Wishlist, Review

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(Review)