from django.shortcuts import redirect


"""
Decoreator for preventing specific types of user List ()
# Pages for different user-roles & the prevent list

1. dec_system_admin
sys-admins => if not (is_superuser, is_admin, is_staff) holei access pabe
(the following users will be prohibited)
Restaurant Owner, Rest. Staff, Regular Users, Anonymous User
Access Role:  (is_superuser, is_admin, is_staff)


2. def_restaurant_owner 
rest-owners => if (is_restaurant_staff, is_regular_user, is_anonymous_user) hole access pabe na
(the following users will be prohibited)
Rest Staff, Regular Cust, Anonymous User
Access Role:   (is_superuser, is_admin, is_staff), is_restaurant_owner


3. dec_restaurant_staff
rest-staffs => if (is_regular_user, is_anonymous_user) hole access pabe na
(the following users will be prohibited)
Regular Cust, Anonymous User
Access Role:   (is_superuser, is_admin, is_staff), is_restaurant_owner, is_restaurant_staff


4. dec_regular_customer 
regu-cust => if (is_anonymous_user, is_restaurant_owner, is_restaurant_staff) hole access pabe na
(the following users will be prohibited)
Anonymous User, Rest. Owner, Rest. Staff
Access Role:   (is_superuser, is_admin, is_staff), is_regular_user


5. dec_anonymous_user (Develop Later)
(the following users will be prohibited)
Anony-User => if (is_regular_user, is_restaurant_owner, is_restaurant_staff) hole access pabe na
Regular Users, Rest Owner, Rest Staff
Access Role:   (is_superuser, is_admin, is_staff), is_anonymous_user


Default Landing Pages (based on user-type):
    (system_admin) --> system admin landing page
    (restOwner_user) --> restaurant owner landing page
    (restStaff_user) --> restaurant staff landing page
    (regular_user) --> regular user landing page
    (anonymous_user) --> regular user landing page
"""



# Stop authenticated/ logged-in users
def stop_authenticated_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            # return redirect('homeApplication:homepage')  # Default homepage for anonymous user
            # [ FURTHER DEVELOPMENT ]: Add msg along with the redirection.
            return redirect('userAuth:common_redirect_page_after_login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func




# Stop restaurant-owner users
def stop_rest_owner(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_restaurant_owner:
            # return redirect('homeApplication:homepage')  # Default homepage for anonymous user
            # [ FURTHER DEVELOPMENT ]: Add msg along with the redirection.
            return redirect('restOwnerApp:rowner_homepage')  # TESTING OK
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func




# Stop restaurant-staff users (Approved Staffs)
def stop_rest_staff(view_func):
    def wrapper_func(request, *args, **kwargs):
        # if request.user.is_restaurant_staff:
        if request.user.is_restaurant_staff and request.user.is_approved:
            # return redirect('homeApplication:homepage')  # Default homepage for anonymous user
            # [ FURTHER DEVELOPMENT ]: Add msg along with the redirection.
            # return redirect('userAuth:res_staff_homepage')  # TESTING OK
            return redirect('restStaffApp:rstaff_homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



# -----------------------------------------------[will test later]
# Stop restaurant-staff users (Not Approved Yet/ Pending Staffs)
def stop_rest_staff_unapproved(view_func):
    def wrapper_func(request, *args, **kwargs):
        # if request.user.is_authenticated and not request.user.is_approved:
        # if request.user.is_authenticated:
        #     if request.user.is_approved:
        #         return redirect('userAuth:res_staff_homepage')
        #     else:
        #         return redirect('userAuth:res_staff_unapproved_homepage')
            #     # return redirect('homeApplication:homepage')  # Default homepage for anonymous user
            #     # [ FURTHER DEVELOPMENT ]: Add msg along with the redirection.
        if not request.user.is_approved:
            return redirect('userAuth:res_staff_unapproved_homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
# -----------------------------------------------



# Stop regular customer users
def stop_regular_cust(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_regular_user:
            # return redirect('homeApplication:homepage')  # Default homepage for anonymous user
            # [ FURTHER DEVELOPMENT ]: Add msg along with the redirection.
            return redirect('userAuth:regular_cust_homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func




# Stop anonymous customer users
def stop_anonymous_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # return redirect('homeApplication:homepage')  # Default homepage for anonymous user
            # [ FURTHER DEVELOPMENT ]: Add msg along with the redirection.
            return redirect('userAuth:common_redirect_page_before_login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func










# Stop un-authenticated/ logged-out users
# def stop_unauthenticated_users(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             # return redirect('homeApplication:homepage')  # Default homepage for anonymous user
            
#             # later to the login-page
#             return redirect('userAuth:common_redirect_page_before_login')  
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func


# # Stop any user other than the systems administrator [access for system admins] - system administrator
# def dec_system_admin(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         # checking users other than sys-admins
#         # try:
#             if not request.user.is_superuser or not request.user.is_admin or not request.user.is_staff:
#                 return redirect('userAuth:common_redirect_page_after_login')
#             else:
#                 return view_func(request, *args, **kwargs)
#         # except:
#         #     return view_func(request, *args, **kwargs)
#     return wrapper_func


# # Stop the restaurant staffs, customers [access for admins, restaurant-owners] - restaurant owners
# def dec_restaurant_owner(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         # checking users other than sys-admins
#         # if request.user.is_restaurant_staff or request.user.is_regular_user or request.user.is_anonymous_user:
#         if not request.user.is_restaurant_owner:
#             return redirect('userAuth:common_redirect_page_after_login')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func


# # Stop the customers [access for admins, restaurant-owners, restaurant staffs] - restaunrant staffs
# def dec_restaurant_staff(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         # checking users other than sys-admins
#         if not request.user.is_restaurant_staff or not request.user.is_restaurant_owner:
#             return redirect('userAuth:common_redirect_page_after_login')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func


# # Stop the restaurant-owners, restaurant staffs [access for admins, customers] - customers
# def dec_regular_customer(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         # checking users other than sys-admins
#         if not request.user.is_regular_user:
#             return redirect('userAuth:common_redirect_page_after_login')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func


# def dec_anonymous_user(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         # checking users other than sys-admins
#         if not request.user.is_anonymous_user:
#             return redirect('userAuth:common_redirect_page_before_login')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func
