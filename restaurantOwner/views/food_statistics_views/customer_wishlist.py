from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import *
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.models import *
from django.db.models import Q  # to make complex queries, if not found, throws an exceptionError
from food.models import *




# ------------------------------------------------------
# Build up the view func firstly, then assign decorators for the restaunrat owner according to the "foodsystem/authentication/auth_testing_views.py" file.
# ------------------------------------------------------




# This homepage for restaunrant owner & staff is using the same base template from "foodsystem/templates/base_restaurant_staff.html"
# This view-func is for the restaurant owner

# @login_required(login_url='userAuth:login')
# @stop_rest_staff
# @stop_regular_cust
# @stop_anonymous_user
# @stop_rest_staff_unapproved

def restaurant_customer_wishlist(request):
    print('Customer Wishlist Page is called!')

    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user_type identification func from the "foodsystem/authentication/helper_functions/identify_user_type.py" files.
    user_type = get_user_type(request.user) # Get the user-type; whether the user is a staff/ customer

    print(request.user.id)
    # Get user profile of this specific restaurant-staff
    u_id = request.user.id

    # Collect the user-profile of the restaurant-Owner
    u_profile = UserProfile.objects.get(id=u_id)

    print(u_profile.bio)
    print(u_profile.profile_pic)



    # get the restaurant-instance from the "CustomUser" model
    restaurantInstance = CustomUser.objects.get(pk=userInfo.id)
    print('Restaurant Instance: ', restaurantInstance)
    print('Restaurant Instance - Restaurant Name: ', restaurantInstance.restaurant_name)


    # # get all the food-instances of the current restaurant
    # foods = Food.objects.filter(created_by=restaurantInstance)
    # # get all the food-like-instances of the current restaurant-food


    # foodLikesInstancesList = []
    # # make a for-loop in the foods-queryset, and inside it, make another query in the "FoodLikes" db-model
    # for fd in foods:
    #     fLikesInstances = FoodLikes.objects.filter(
    #         food_id=fd
    #         ,is_liked=True
    #     )
    #     for fli in fLikesInstances:
    #         foodLikesInstancesList.append(fli)
    #         # foodLikesInstancesList += fli


    # print('x'*20)
    # for flil in foodLikesInstancesList:
    #     print('Liked Food Instances: ', flil)
    #     print('Liked Food Instances (Type): ', type(flil))
    # print('x'*20)

    # slightly modified
    customerLovedFood = FoodLikes.objects.all()



    # user_profile_exist = False

    # # Check if there is any profile-picture exists.
    # if u_profile.profile_pic:
    #     user_profile_exist = True
        
    # default_user_profile_pic = 'foodsystem\media\profilePicture\default_dp.png'
    # default_user_profile_pic = 'foodsystem.media.profilePicture.default_dp.png'


    context = {
        'title': 'Restaurant Owner HomePage',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,


        'customerLovedFood': customerLovedFood,
        # 'rest_profile': rest_profile,
        # 'user_profile_exist': user_profile_exist,
        # 'default_user_profile_pic': default_user_profile_pic,
    }
    # This homepage is specifically for the restaurant owners
    return render(request, 'restaurantOwner/customer_wishlist.html', context)
