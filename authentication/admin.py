from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class CustomUserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'company_name', 'restaurant_name', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active', 'is_approved', 'is_staff', 'is_admin', 'is_superuser', 'is_restaurant_owner', 'is_restaurant_staff', 'is_regular_user', 'is_anonymous_user']
    list_display_links = ['email']
    search_fields = ['email', 'company_name', 'first_name', 'last_name', 'phone', 'restaurant_id']
    readonly_fields = ['restaurant_id', 'date_joined', 'last_login'] # to view these fields in the "User List" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields. Also, make sure to make the restaurant_id immutable
    filter_horizontal = []
    fieldsets = []
    list_filter = ['last_login', 'is_superuser', 'is_admin', 'is_staff', 'is_restaurant_owner', 'is_restaurant_staff', 'is_approved', 'is_regular_user', 'is_anonymous_user']
    list_per_page = 15
    ordering = ['email']

    add_fieldsets = [
        (None, {
            'classes':('wide'),
            'fields':('email', 'company_name', 'phone', 'password1', 'password2'),
        })
    ]





# class RestaurantOwnerAdmin(admin.ModelAdmin):
#     list_display = ['restaurant_name', 'email', 'first_name', 'last_name', 'phone', 'tin_number', 'date_joined', 'last_login', 'is_restaurant_owner', 'is_restaurant_staff', 'is_active', 'is_staff', 'is_admin', 'is_superuser']
#     list_display_links = ['restaurant_name']
#     search_fields = ['email', 'restaurant_name', 'first_name', 'last_name', 'phone', 'tin_number']
#     readonly_fields = ['date_joined', 'last_login'] # to view these fields in the "User List" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
#     filter_horizontal = []
#     fieldsets = []
#     list_filter = ['last_login']
#     list_per_page = 20
#     ordering = ['restaurant_name']

#     add_fieldsets = [
#         (None, {
#             'classes':('wide'),
#             'fields':('email', 'restaurant_name', 'phone', 'password1', 'password2'),
#         })
#     ]





# class RestaurantStaffAdmin(admin.ModelAdmin):
#     list_display = ['email', 'first_name', 'last_name', 'phone', 'restaurant', 'date_joined', 'last_login', 'is_restaurant_owner', 'is_restaurant_staff', 'is_active', 'is_staff', 'is_admin', 'is_superuser']
#     list_display_links = ['restaurant']
#     search_fields = ['email', 'restaurant', 'first_name', 'last_name', 'phone']
#     readonly_fields = ['date_joined', 'last_login'] # to view these fields in the "User List" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
#     filter_horizontal = []
#     fieldsets = []
#     list_filter = ['last_login']
#     list_per_page = 20
#     ordering = ['restaurant']

#     add_fieldsets = [
#         (None, {
#             'classes':('wide'),
#             'fields':('email', 'restaurant', 'phone', 'password1', 'password2'),
#         })
#     ]


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(RestaurantOwner, RestaurantOwnerAdmin)
# admin.site.register(RestaurantOwner)
# admin.site.register(RestaurantStaff, RestaurantStaffAdmin)