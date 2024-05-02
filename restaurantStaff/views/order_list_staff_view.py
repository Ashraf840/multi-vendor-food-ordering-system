from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from cartOrder.models import *
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.models import *
from cartOrder.forms import *
from django.urls.base import reverse
from django.db.models import Q








# [ Decorators ]
# restaurant staffs will also be able to access this pages.
def orderList_staff_view(request):
    print('Restaurant Order List (Staff View) Page is called!')

    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user_type identification func from the "foodsystem/authentication/helper_functions/identify_user_type.py" files.
    user_type = get_user_type(request.user) # Get the user-type; whether the user is a staff/ customer

    # Get user profile of this specific restaurant-staff
    u_id = request.user.id

    # Collect the user-profile of the restaurant-Owner
    u_profile = UserProfile.objects.get(id=u_id)



    # get the restaurant-staff-instances from the "CustomeUser" model
    print('Staff\'s Restaurant ID: ', request.user.restaurant_id)

    # get the restaurant-instance from the "CustomeUser" model
    restaurantIntance = CustomUser.objects.get(
        Q(restaurant_id=request.user.restaurant_id)
        & Q(is_restaurant_owner=True)
    )

    print('x'*20)
    print('Restaurant: ', restaurantIntance.restaurant_name)
    print('x'*20)


    # get the food-order-instances based of the restaurant-instance
    restOrder = Order.objects.filter(restaurant=restaurantIntance.restaurant_name).all().order_by('-id')
    total_order_num = len(restOrder)







    # restOrder = Order.objects.filter(restaurant=userInfo.restaurant_name).all().order_by('-id')
    # total_order_num = len(restOrder)
    # # for rOrd in restOrder:
    # #     print(rOrd)



    context = {
        'title': 'Food Orders',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,

        'restOrder': restOrder,
        'total_order_num': total_order_num,
    }
    return render(request, 'restaurantStaff/order_list_staff_view.html', context)



