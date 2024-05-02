from django.shortcuts import render
from .decorators import *
from django.contrib.auth.decorators import login_required


"""
--------------------------------------------
This file is used as a reference for using decorators in different application views.
--------------------------------------------
"""


# Create your views here.
# Check System Admin Decorator
# @stop_unauthenticated_users

# @dec_system_admin
@login_required(login_url='userAuth:login')
@stop_rest_owner
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def check_sysAdmin(request):
    context = {
        'title': 'Sys Admin',
    }
    return render(request, 'testing_auth/system_admin.html', context)


# Check Restaurant Owner Decorator
# @stop_unauthenticated_users
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def check_res_owner(request):
    context = {
        'title': 'Restaurant Owner',
    }
    return render(request, 'testing_auth/restaurant_owner.html', context)


# Check Restaurant Staff Decorator
# @stop_unauthenticated_users
@login_required(login_url='userAuth:login')
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def check_res_staff(request):
    context = {
        'title': 'Restaurant Staff',
    }
    return render(request, 'testing_auth/restaurant_staff.html', context)



# Check Restaurant Staff (unapproved/ pending) Decorator
@login_required(login_url='userAuth:login')
@stop_rest_owner
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
# @stop_rest_staff_unapproved
def check_res_staff_unapproved(request):
    context = {
        'title': 'Restaurant Staff - Unapproved/ Pending',
    }
    return render(request, 'testing_auth/restaurant_staff_unapproved.html', context)




# Check Regular Customer Decorator
# @stop_unauthenticated_users
@login_required(login_url='userAuth:login')
@stop_rest_owner
@stop_rest_staff
@stop_anonymous_user
@stop_rest_staff_unapproved
def check_regularCust(request):
    context = {
        'title': 'Regular Customer',
    }
    return render(request, 'testing_auth/customer.html', context)




# Check Anonymous Customer Decorator
# @stop_unauthenticated_users
@stop_anonymous_user
@stop_regular_cust
@stop_rest_owner
@stop_rest_staff
@stop_rest_staff_unapproved
def check_anonymousCust(request):
    context = {
        'title': 'Anonynous User',
    }
    return render(request, 'testing_auth/anonymous_customer.html', context)


# Redirected all users to this common redirected page
@stop_authenticated_users
def common_redirect_page_before_login(request):
    context = {
        'title': 'Un-authenticated User',
    }
    return render(request, 'testing_auth/common_redirected_page_before_login.html', context)


# @stop_unauthenticated_users
@login_required(login_url='userAuth:login')
def common_redirect_page_after_login(request):
    context = {
        'title': 'Authenticated User',
    }
    return render(request, 'testing_auth/common_redirected_page_after_login.html', context)
