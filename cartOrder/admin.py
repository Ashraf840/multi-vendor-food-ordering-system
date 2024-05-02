from django.contrib import admin
from .models import *



class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'restaurant', 'cart_id', 'is_ordered', 'total_cart_items', 'total_price', 'created_at', 'last_updated_at']
    list_display_links = ['customer']
    search_fields = ['restaurant', 'cart_id', 'created_at', 'last_updated_at']
    readonly_fields = ['created_at', 'last_updated_at']  # to view these fields in the "(Food) Category" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['is_ordered', 'created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['customer']




class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_id', 'cartItem_id', 'food', 'price', 'quantity', 'created_at', 'last_updated_at']
    list_display_links = ['cart_id']
    search_fields = ['cart_id', 'cartItem_id', 'created_at', 'last_updated_at']
    readonly_fields = ['created_at', 'last_updated_at']  # to view these fields in the "(Food) Category" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['cart_id']




class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'cart_id', 'order_id', 'restaurant', 'price', 'payment_method', 'status', 'is_cancelled', 'is_paid', 'delivery_address', 'delivery_time', 'created_at', 'last_updated_at']
    list_display_links = ['customer']
    search_fields = ['order_id', 'created_at', 'last_updated_at']
    readonly_fields = ['delivery_time', 'created_at', 'last_updated_at']  # to view these fields in the "(Food) Category" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['delivery_time', 'created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['customer']




admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
