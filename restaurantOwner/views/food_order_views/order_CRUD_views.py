from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from cartOrder.models import *
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.models import *
from cartOrder.forms import *
from django.urls.base import reverse




# [ Decorators ]
# restaurant staffs will also be able to access this pages.
def orderList(request):

    print('Restaurant Name: ', request.user.restaurant_name)

    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user_type identification func from the "foodsystem/authentication/helper_functions/identify_user_type.py" files.
    user_type = get_user_type(request.user) # Get the user-type; whether the user is a staff/ customer

    # Get user profile of this specific restaurant-staff
    u_id = request.user.id

    # Collect the user-profile of the restaurant-Owner
    u_profile = UserProfile.objects.get(id=u_id)


    restOrder = Order.objects.filter(restaurant=userInfo.restaurant_name).all().order_by('-id')
    total_order_num = len(restOrder)
    # for rOrd in restOrder:
    #     print(rOrd)



    context = {
        'title': 'Food Orders',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,

        'restOrder': restOrder,
        'total_order_num': total_order_num,
    }
    return render(request, 'restaurantOwner/order_list.html', context)





# restaurant staffs will also be able to access this pages.
def restaurant_order_status_update(request, order_id):
    print('Restaurant Name: ', request.user.restaurant_name)

    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user_type identification func from the "foodsystem/authentication/helper_functions/identify_user_type.py" files.
    user_type = get_user_type(request.user) # Get the user-type; whether the user is a staff/ customer

    # Get user profile of this specific restaurant-staff
    u_id = request.user.id

    # Collect the user-profile of the restaurant-Owner
    u_profile = UserProfile.objects.get(id=u_id)


    # restOrder = Order.objects.filter(restaurant=userInfo.restaurant_name).all().order_by('-id')
    # total_order_num = len(restOrder)
    # for rOrd in restOrder:
    #     print(rOrd)
    

    order = Order.objects.filter(order_id=order_id).first()

    order_user_full_name = order.customer.first_name + ' ' + order.customer.last_name
    # print(order.user.first_name)
    # print('%s %s' % (order.user.first_name, order.user.last_name))

    form = OrderStatusUpdateForm(instance=order)

    # If no such order with this order_id is found, redirect user to the home-page.
    if order is None:
        return redirect('restOwnerApp:food_order_list')

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(request.get_full_path())    # redirect to the same page


    context = {
        'title': 'Food Orders',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,

        'order': order,
        'orderForm': form,
        'user_full_name': order_user_full_name,
    }
    return render(request, 'cartOrder/order_stat_updation.html', context)







# [ Decorator ]
# restaurant staffs will also be able to access this pages.
def restaurant_order_paidUnpaid_update(request, order_id):
    # print('Order Paid/Unpaid is called!')
    # print('Order ID: ', order_id)

    # get the order-instance
    orderInstance = Order.objects.get(order_id=order_id)
    # print('Order Instance: ', orderInstance)
    orderInstance.is_paid = True
    orderInstance.save()

    return redirect(reverse(
        'restOwnerApp:restaurant_order_status_update', 
        kwargs={"order_id": order_id}
    ))


