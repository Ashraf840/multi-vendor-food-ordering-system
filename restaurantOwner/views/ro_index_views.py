from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import *
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.models import *




# ------------------------------------------------------
# Build up the view func firstly, then assign decorators for the restaunrat owner according to the "foodsystem/authentication/auth_testing_views.py" file.
# ------------------------------------------------------




# This homepage for restaunrant owner & staff is using the same base template from "foodsystem/templates/base_restaurant_staff.html"
# This view-func is for the restaurant owner
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def restaurant_owner_homepage(request):
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


    # Collect the restaurant-profile of the restaurant
    rest_profile = RestaurantProfile.objects.get(id=u_id)
    print('*'*10)
    print(rest_profile.opening_time)
    print(rest_profile.closing_time)
    print(rest_profile.restaurant_profile_pic)


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
        'rest_profile': rest_profile,
        # 'user_profile_exist': user_profile_exist,
        # 'default_user_profile_pic': default_user_profile_pic,
    }
    # This homepage is specifically for the restaurant owners
    return render(request, 'restaurantOwner/index.html', context)
    # return render(request, 'base_restaurant_owner_staff.html', context)
    # return render(request, 'base.html', context)
