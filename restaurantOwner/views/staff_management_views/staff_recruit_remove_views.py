from django.shortcuts import redirect, render
from authentication.models import CustomUser
from django.contrib.auth import get_user_model
from django.db.models import Q  # to make complex queries
from authentication.helper_functions.identify_user_type import get_user_type
from django.contrib.auth.decorators import login_required
from authentication.decorators import *
from django.http import HttpResponseRedirect
from userProfile.models import UserProfile
from userProfile.helper_functions.export_user_profile import export_user_profile
from django.core.paginator import Paginator




"""
----------------------------------------------
>>>>> The following views will primarily grant access for the AUTHENTICATED users

Access Roles to the following views of this page:  System Admins, Restaurant Owners
----------------------------------------------
"""



@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved  # test it using loggin in the system using an unapproved_rstaff
def staff_list(request):
    userInfo = request.user

    print('Restaurant Name: %s' % userInfo.restaurant_name)
    print('User fullname: %s %s' % (userInfo.first_name, userInfo.last_name))
    print('User Type: %s' % get_user_type(userInfo))

    rest_name = userInfo.restaurant_name
    user_fullname = userInfo.first_name + ' ' + userInfo.last_name
    user_type = get_user_type(userInfo)

    # print('Company Name: %s' % userInfo.company_name)
    # print('Email: %s' % userInfo.email)

    # Don't need a queryset, cause later it'll be complex to make another query using the queryset to fetch all the rest_staff having same restaurant_id.
    # user_detail = CustomUser.objects.filter(
    #     Q(email=userInfo.email)
    # )

    # Get the specific class-object of the restaurant-owner (Specific user-data)
    user_detail = CustomUser.objects.get(
        Q(email=userInfo.email)
    )

    # Fetch the Restaurant ID, so that it can be passed to the "base_restaurant_owner.html" -> the inline-js -> searchStaff_api.js
    rest_id = user_detail.restaurant_id
    print("%s Restaurant ID: %s %s" % ( ('*'*10), (rest_id), ('*'*10) ))
    # print(rest_id)

    # print('Type: %s' % type(user_detail))
    print('type %s' % type(user_detail))
    print('Account Status %s' % user_detail.is_approved)

    print(user_detail.restaurant_id)    # get the current restaurant owners restaurant_id

    # Make a queryset consists of all the users who are restaurant staff & contains the same restaurant_id
    rest_staffs = CustomUser.objects.filter(
        Q(restaurant_id=user_detail.restaurant_id) &
        Q(is_restaurant_staff=True)
    ).all()


    print("%s All staffs List (specific restaurant) %s" % ( ('*'*10), ('*'*10) ))
    for rs_users in rest_staffs:
        print(rs_users)
    print("%s %s %s" % ( ('*'*10), ('x'*5), ('*'*10) ))




    # for q in user_detail:
    #     print(q.restaurant_id)



    # for f in CustomUser._meta.get_fields():
    #     print(f)

    # rest_id = 'restaurant_id'
    # obj = CustomUser.objects.first()
    # field_obj = CustomUser._meta.get_field(rest_id)
    # field_value = getattr(obj, field_obj.attname)
    # print(field_value)


    """
    # Print user details in the terminal
    print('\n')
    print('%s Printing User Details in the terminal %s' % ( ('*'*10), ('*'*10) ))
    print(type(userInfo))

    print('User ID: %s' % userInfo.id)

    print('Email: %s' % userInfo.email)
    print('Company Name: %s' % userInfo.company_name)
    
    print('First Name: %s' % userInfo.first_name)
    print('Last Name: %s' % userInfo.last_name)
    print('Gender: %s' % userInfo.gender)
    
    # -----------------
    # print('Restaurant Name: %s' % userInfo.restaurant_name)
    print('Restaurant ID: %s' % userInfo.restaurant_id)
    print('TIN Num: %s' % userInfo.tin_number)
    print('Phone: %s' % userInfo.phone)
    
    print('Date Joined: %s' % userInfo.date_joined)
    print('Last Login: %s' % userInfo.last_login)

    print('Active: %s' % userInfo.is_active)
    print('System Staff: %s' % userInfo.is_staff)
    print('System Admin: %s' % userInfo.is_admin)
    print('System Superuser: %s' % userInfo.is_superuser)
    print('Restaurant Owner: %s' % userInfo.is_restaurant_owner)
    print('Restaurant Staff: %s' % userInfo.is_restaurant_staff)
    print('Regular User/ Customer: %s' % userInfo.is_regular_user)
    print('Anonymous User: %s' % userInfo.is_anonymous_user)
    
    print('Approved: %s' % userInfo.is_approved)

    print('%s %s %s' % ( ('*'*10), ('x'*5), ('*'*10) ))
    print('\n')

    
    # Make query to fetch the restaurant owners user-detail from the backend
    # rest_user = CustomUser.objects.get(email=userInfo.email)
    rest_user = get_user_model()
    print('Restaurant: %s' % type(rest_user))
    print('Restaurant Name: %s' % (rest_user.restaurant_name))

    # for rownu in rest_user.values():
    #     print(rownu)
    """


    # User = get_user_model()
    # source = User.objects.get(id=User.id)
    # recipient = User.objects.get(id=message['recipient'])
    # print('Source: %s' % source)
    # print('Source: %s' % User.restaurant_id)

    # print('User Name: %s' % (request.user.restaurant_id))

    # user_detail = CustomUser.objects.get(email=request.user.email)
    # print('Type: %s' % type(user_detail))
    # print('Restaurant ID: %s' % user_detail.restaurant_id)


    # [ HELPER FUNCTION ]: to grab the user-profile-data
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    # u_profile = UserProfile.objects.get(id=u_id)
    u_profile = export_user_profile(userID = u_id)


    # Restaurant Staff Paginator
    rest_staff_paginator = Paginator(rest_staffs, 5)
    rest_staff_page = request.GET.get('page')
    paginated_rest_staff_list_query = rest_staff_paginator.get_page(rest_staff_page)
    rest_staffs = paginated_rest_staff_list_query

    print(paginated_rest_staff_list_query)

    context={
        'title': 'RO - Staff List (All)',
        'rest_name': rest_name,
        'user_fullname': user_fullname,
        'user_type': user_type,
        'rest_staffs': rest_staffs,
        'rest_id': rest_id,
        'u_profile': u_profile,
        'rest_staff_paginator': paginated_rest_staff_list_query,
    }
    return render(request, 'restaurantOwner/staff_list.html', context)







@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def staff_list_pending(request):
    userInfo = request.user

    """
    # # for testing purpose
    # print('Restaurant Name: %s' % userInfo.restaurant_name)
    # print('User fullname: %s %s' % (userInfo.first_name, userInfo.last_name))
    # print('User Type: %s' % get_user_type(userInfo))
    """

    rest_name = userInfo.restaurant_name
    user_fullname = userInfo.first_name + ' ' + userInfo.last_name
    user_type = get_user_type(userInfo)

    # user_detail = CustomUser.objects.filter(
    #     Q(email=userInfo.email)
    # )

    # Get the single row users-data-object (class-obj, not a queryset)
    user_detail = CustomUser.objects.get(
        Q(email=userInfo.email)
    )

    # Fetch the Restaurant ID
    rest_id = user_detail.restaurant_id
    print("%s Restaurant ID: %s %s" % ( ('*'*10), (rest_id), ('*'*10) ))
    # print(rest_id)

    # for testing purpose
    # print(user_detail.restaurant_id)    # get the current restaurant owners restaurant_id

    # Make a queryset consists of all the users who are restaurant staff, inactive, & contains the same restaurant_id
    rest_staffs = CustomUser.objects.filter(
        Q(restaurant_id=user_detail.restaurant_id) &
        Q(is_restaurant_staff=True) &
        Q(is_approved=False)
    ).all()

    """
    # # for testing purpose
    # print("%s All staffs List (specific restaurant) %s" % ( ('*'*10), ('*'*10) ))
    # for rs_users in rest_staffs:
    #     print(rs_users)
    # print("%s %s %s" % ( ('*'*10), ('x'*5), ('*'*10) ))
    """

    # [ HELPER FUNCTION ]: to grab the user-profile-data
    # Get the user-profile model (intially get the user-profile-picture)
    u_id = request.user.id
    # u_profile = UserProfile.objects.get(id=u_id)
    u_profile = export_user_profile(userID = u_id)


    context={
        'title': 'RO - Staff List (Pending)',
        'rest_name': rest_name,
        'user_fullname': user_fullname,
        'user_type': user_type,
        'u_profile': u_profile,

        # For Search Staff API
        'rest_staffs': rest_staffs,
        'userInfo': userInfo,
    }
    return render(request, 'restaurantOwner/staff_list_pending.html', context)






# Suspend restaurant staff
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
# Views without using a dj-form to interact with the DB (more like the "remove" method)
def restStaff_suspend(request, id):
    rest_staff = CustomUser.objects.get(pk=id)
    rest_staff.is_approved = False
    rest_staff.save()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('restOwnerApp:rowner_staff_list')








# Unsuspend restaurant staff
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
# Views without using a dj-form to interact with the DB (more like the "remove" method)
def restStaff_unsuspend(request, id):
    rest_staff = CustomUser.objects.get(pk=id)
    rest_staff.is_approved = True
    rest_staff.save()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('restOwnerApp:rowner_staff_list')







# Approve Restaurant Staffs
# Only restaurant owner & system admin can use this view/ func
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def staff_approval(request, id):
    p_staff = CustomUser.objects.get(pk=id)

    print("%s %s %s" % ( ('*'*10), ('x'*5), ('*'*10) ))
    print("Staff ID: %s" % p_staff.id)
    print("Staff Name: %s" % p_staff)
    print("Staff Approval Status: %s" % p_staff.is_approved)
    print("%s %s %s" % ( ('*'*10), ('x'*5), ('*'*10) ))
    
    
    # p_staff.is_approved = True
    # print("Staff Approval Status (after): %s" % p_staff.is_approved)


    # Try not to hit the DB un-necessarily
    if not p_staff.is_approved:
        # approve staffs individually (only for the specific restaurant)
        # Solution to update a single row of the DB model/ table:   https://stackoverflow.com/a/2712871
        CustomUser.objects.filter(pk=id).update(is_approved = True)
    else:
        print('%s The restaurant staff is already approved in the restaurant domain!  %s' % ( ('*'*10), ('*'*10) ))
        return redirect('restaurantOwnerApplication:rowner_pending_staff_list')


    return redirect('restaurantOwnerApplication:rowner_pending_staff_list')






# Delete Restaurant Staff
# Only restaurant owner & system admin can use this view/ func
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def delete_staff(request, id):
    staff = CustomUser.objects.get(pk=id)
    staff.delete()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('restaurantOwnerApplication:rowner_staff_list')
