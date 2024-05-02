from django.contrib import admin
from .models import *



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio', 'profile_pic']
    list_display_links = ['user']
    search_fields = ['user']
    filter_horizontal = []
    fieldsets = []
    list_per_page = 15
    ordering = ['user']



class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'opening_time', 'closing_time', 'is_closed', 'restaurant_profile_pic', 'created_at', 'last_updated_at']
    list_display_links = ['user']
    # list_editable = [ 'opening_time', 'closing_time' ]
    search_fields = ['user']
    filter_horizontal = []
    fieldsets = []
    list_per_page = 15
    ordering = ['user']



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RestaurantProfile, RestaurantProfileAdmin)
