from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from cartOrder.models import *
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.models import *
from cartOrder.forms import *
from django.urls.base import reverse
from django.db.models import Q  # to make complex queries, if not found, throws an exceptionError







# [ Decorators ]
# restaurant staffs will also be able to access this pages.
# Food that are not received by the customers, will be in the pending list.
def pendingOrderList(request):
    print('Pending Order List Page is called!')
    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user_type identification func from the "foodsystem/authentication/helper_functions/identify_user_type.py" files.
    user_type = get_user_type(request.user) # Get the user-type; whether the user is a staff/ customer

    # Get user profile of this specific restaurant-staff
    u_id = request.user.id

    # Collect the user-profile of the restaurant-Owner
    u_profile = UserProfile.objects.get(id=u_id)

    # get the user-instance from the "CustomUser" model
    print('Restaurant User ID (CustomUser): ', userInfo.id)
    restaurantInstance = CustomUser.objects.get(pk=userInfo.id)
    print('Restaurant Instance: ', restaurantInstance)
    print('Restaurant Instance - Restaurant Name: ', restaurantInstance.restaurant_name)


    # get all the orders from the "Order" model inside the "cartOrder" application.
    # The orders status should not be the "Order Received by Customer", thus those orders will be counted as pending-orders.
    pendingOrders = Order.objects.filter(
        Q(restaurant=restaurantInstance.restaurant_name)
        & Q(status="Order Received by Restaurant")
        | Q(status="Baking")
        | Q(status="Baked")
        | Q(status="Out for Delivery")
    )

    print('x'*20)
    for po in pendingOrders:
        print('Restaurant Pending Order: ', po)
    print('x'*20)

    total_pending_order_num = len(pendingOrders)


    context = {
        'title': 'Order List: Pending',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,

        'pendingOrders': pendingOrders,
        'total_pending_order_num': total_pending_order_num,
    }
    return render(request, 'restaurantOwner/pending_order.html', context)
    # return HttpResponse('Pending Order List Page is called!')


