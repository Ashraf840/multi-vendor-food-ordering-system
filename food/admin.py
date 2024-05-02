from django.contrib import admin
from .models import *



class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name', 'created_by', 'date_created']
    list_display_links = ['tag_name']
    search_fields = ['tag_name']
    readonly_fields = ['date_created']  # to view these fields in the "(Food) Category" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['date_created']
    list_per_page = 15
    ordering = ['tag_name']




class CategoryAdmin(admin.ModelAdmin):
    # list_display = ['id', 'cate_name', 'created_by', 'created_at', 'last_updated_at']
    list_display = ['id', 'cate_name', 'created_at', 'last_updated_at']
    list_display_links = ['cate_name']
    search_fields = ['cate_name']
    readonly_fields = ['created_at', 'last_updated_at'] # to view these fields in the "(Food) Category" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['cate_name']




class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'food_name', 'category', 'created_by', 'reward_point', 'price', 'food_code', 'is_available', 'created_at', 'last_updated_at']
    list_display_links = ['food_name']
    search_fields = ['food_name', 'reward_point', 'price', 'food_code']
    readonly_fields = ['created_at', 'last_updated_at'] # to view these fields in the "Food" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['created_at', 'last_updated_at', 'is_available']
    list_per_page = 15
    ordering = ['food_name']





class AddonAdmin(admin.ModelAdmin):
    list_display = ['id', 'addon_name', 'created_by', 'price', 'created_at', 'last_updated_at']
    list_display_links = ['addon_name']
    search_fields = ['addon_name']
    readonly_fields = ['created_at', 'last_updated_at'] # to view these fields in the "Food" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['addon_name']






class FoodRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'food_id', 'rating', 'created_at', 'last_updated_at']
    list_display_links = ['customer_id']
    search_fields = ['id']
    readonly_fields = ['created_at', 'last_updated_at'] # to view these fields in the "Food" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['customer_id']





class FoodLikesAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'food_id', 'is_liked', 'created_at', 'last_updated_at']
    list_display_links = ['customer_id']
    search_fields = ['id']
    readonly_fields = ['is_liked', 'created_at', 'last_updated_at'] # to view these fields in the "Food" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['customer_id']



admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Addon, AddonAdmin)
admin.site.register(FoodRating, FoodRatingAdmin)
admin.site.register(FoodReview)
admin.site.register(ReviewHelpful)
admin.site.register(FoodLikes, FoodLikesAdmin)
admin.site.register(ComboMeal)
