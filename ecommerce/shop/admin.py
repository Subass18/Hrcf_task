from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'user']
    search_fields = ['name']
    list_filter = ['category', 'user']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    search_fields = ['user__username']
    list_filter = ['created_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
    list_filter = ['cart', 'product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'ordered_at', 'status']
    list_filter = ['status', 'ordered_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
