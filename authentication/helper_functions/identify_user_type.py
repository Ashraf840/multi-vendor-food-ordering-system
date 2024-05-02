# Custom Func to fetch the full name of the user; 
# need to make it a func, bcz the following steps to gather user's full-name are required in 3 other view-funcs ('index', 'order', 'order_list') to fetch the user's full-name, 
# so I've made this custom-func and then call this func in different view-funcs accross the project according to the requirements.
# def get_username(username):
#     try:
#         user = username     # This will only render the company_name of the user, for which the regular-customer don't have
#         user = user.get_full_name()     # Get the full-name of the logged-in user
#     # Optional to use the 'except'
#     except:
#         user = 'Anonymous User'
    
#     return user


def get_user_type(user):
    try:
        # if user.is_superuser or user.is_admin or user.is_staff:
        if user.is_superuser:
            # print('User Status: Staffs %s' % ('*'*30))
            user_type = 'System Superuser'
        elif user.is_admin:
            user_type = 'System Admin'
        elif user.is_staff:
            user_type = 'System Staff'
        elif user.is_restaurant_owner:
            user_type = 'Restaurant Owner'
        elif user.is_restaurant_staff:
            user_type = 'Restaurant Staff'
        elif user.is_regular_user:
            user_type = 'Regular Customer/ User'
        else:
            # print('User Status: Customer %s' % ('*'*30))
            user_type = 'Anonymous User'
        return user_type
    except:
        # print('User Status: Unknown %s' % ('*'*30))
        user_type = 'Unknown User Type'
        return user_type