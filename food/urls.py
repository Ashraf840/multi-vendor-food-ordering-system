from django.urls import path, include
from .views import (
    food_tag_CRUD_views as ftcv,
    food_category_CRUD_views as fccv,
    food_addon_CRUD_views as facv,
    food_CRUD_views as fcv,
    food_detail_cust_views as fdcv,
)


app_name = 'foodApp'


urlpatterns = [
    # [ Food tag List + Add Food Tag]
    path('food-tag-list/', ftcv.foodTagList, name='food_foodTagList'),  # homepage for both the restaurant owner & staff
    
    # [ Food Tag Delete]
    path('food-tag-delete/<int:id>/', ftcv.foodTagRemove, name='food_foodTagRemove'),  # Food Tag Remove Endpoint for both the restaurant owner & staff

    # [ Food Category List + Add Food Category ]
    path('food-category-list/', fccv.foodCategoryList, name='food_foodCategoryList'),

    # [ Food Category Remove ]
    path('food-category-remove/<int:id>/', fccv.foodCategoryRemove, name='food_foodCategoryRemove'),

    # [ Food Addon List + Add Food Addon ]
    path('food-addon-list/', facv.foodAddonList, name='food_foodAddonList'),

    # [ Food Addon Update: Make addon "Not Avaiable" ]
    path('food-addon-update/make-not-available/<int:id>/', facv.foodAddonStatUpdate_makeUnavailable, name='foodAddonStatUpdate_makeUnavailable'),

    # [ Food Addon Update: Make addon "Avaiable" ]
    path('food-addon-update/make-available/<int:id>/', facv.foodAddonStatUpdate_makeAvailable, name='foodAddonStatUpdate_makeAvailable'),

    # [ Food Addon Remove ]
    path('food-addon-remove/<int:id>/', facv.foodAddonRemove, name='food_foodAddonRemove'),
    
    # [ Food List ]
    path('food-list/', fcv.foodList, name='food_foodList'),
    # [ Food List Recently Added ]
    path('food-list/recently-added/', fcv.foodList_recentlyadded, name='food_foodList_recentlyadded'),

    # [ Create New Food ]
    path('create-food/', fcv.createFood, name='food_createFood'),
    # path('create-food/food-tag-insert/<int:userID>/', fcv.food_tag_insert, name='food_createFood_foodTagInsert'),

    # [ Update Food Detail ]
    path('update-food-detail/<int:id>/', fcv.updateDetailFood, name='food_udpateFoodDetail'),

    # [ Food Record Remove ]
    path('remove-food-record/<int:id>/', fcv.foodRecordRemove, name='food_removeFoodRecord'),


    # [ Food Detail Page - Customer View ]
    path('food-detail/<str:foodID>/<str:cartID>/', fdcv.foodDetail, name='food_detail'),

    # [ Food Detail Page - Update Food Rating - Customer View ]
    path('food-detail/update-rating/<str:foodID>/<str:cartID>/', fdcv.updateFoodRating, name='updateFoodRating'),

    # [ Food Detail Page - Update Food Loved - Customer View ]
    path('food-detail/update-loved/<str:foodID>/<str:cartID>/', fdcv.foodLiked, name='foodLiked'),

    # [ Food Detail Page - Update Food Unloved - Customer View ]
    path('food-detail/update-unloved/<str:foodID>/<str:cartID>/', fdcv.foodUnliked, name='foodUnliked'),
]
