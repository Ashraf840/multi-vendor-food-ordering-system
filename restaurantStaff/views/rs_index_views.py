from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.decorators import *
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.models import UserProfile




# ------------------------------------------------------
# Build up the view func firstly, then assign decorators for the restaunrat owner according to the "foodsystem/authentication/auth_testing_views.py" file.
# ------------------------------------------------------




# This homepage for restaunrant owner & staff is using the same base template from "foodsystem/templates/base_restaurant_staff.html"
# This view-func is for the restaurant owner
@login_required(login_url='userAuth:login')
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def restaurant_staff_homepage(request):
    # Get the user_type identification func from the "foodsystem/authentication/helper_functions/identify_user_type.py" files.
    user_type = get_user_type(request.user) # Get the user-type; whether the user is a staff/ customer

    # Get user profile of this specific restaurant-staff
    u_id = request.user.id
    u_profile = UserProfile.objects.get(id=u_id)


    context = {
        'title': 'Restaurant Staff HomePage',
        'user_type': user_type,
        'u_profile': u_profile,
    }
    # This homepage is specifically for the restaurant staffs, but the 'restaurantStaff/homepage.html' will be using the 'base_restaurant_owner_staff.html' file as a base template.
    return render(request, 'restaurantStaff/index.html', context)
    # return render(request, 'base_restaurant_owner_staff.html', context)
    # return render(request, 'base.html', context)
