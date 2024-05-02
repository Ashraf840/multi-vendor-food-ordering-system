from django.contrib import admin
from .models import *



class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'promo_code_name', 'promo_code', 'is_available', 'rest_owner', 'discount_price', 'created_at', 'last_updated_at']
    list_display_links = ['promo_code_name']
    search_fields = ['promo_code_name', 'promo_code']
    readonly_fields = ['created_at', 'last_updated_at'] # to view these fields in the "Food" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['created_at']
    list_per_page = 15
    ordering = ['promo_code_name']


admin.site.register(PromoCode, PromoCodeAdmin)


