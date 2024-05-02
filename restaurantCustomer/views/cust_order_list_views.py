from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse
from cartOrder.models import *
from authentication.models import *



# [ Decorator ]
def customerOrderList(request):

    # get the customer-instance
    cust = CustomUser.objects.get(email=request.user.email)
    # print(cust_email)

    # get the order-instance(s) based on the customer-instance
    custOrders = Order.objects.filter(customer=cust).all()
    # for o in custOrders:
    #     print(o)

    total_order_num = len(custOrders)


    context = {
        'title': 'My Orders',
        'custOrders': custOrders,
        'total_order_num': total_order_num,
    }
    return render(request, 'restaurantCustomer/cust_order_list.html', context)





def custOrderDetail(request, orderID):
    # print(orderID)

    # get order-instance
    orderInstance = Order.objects.get(order_id=orderID)
    # print('Order Instance: ', orderInstance)
    # print('Order Instance ID: ', orderInstance.order_id)

    # get the cartItem-instance
    cartItemInstance = CartItem.objects.filter(cart_id=orderInstance.cart_id).all()
    # for cit in cartItemInstance:
    #     print('CartItem Instance: ', cit)
    

    context = {
        'title': 'Order Detail',
        'cartItemInstance': cartItemInstance,
        'orderInstance': orderInstance,
    }
    return render(request, 'restaurantCustomer/cust_order_detail.html', context)




# [ Decorator ]
def orderCancel(request, orderID):
    # print('orderInstance - orderID: ', orderID)
    # get the order-instance
    orderInstance = Order.objects.get(order_id=orderID)
    # print('orderInstance - cancel def: ', orderInstance)
    orderInstance.is_cancelled = True
    orderInstance.save()

    return redirect(reverse(
        'restCustApp:customerfoodOrderDetail', 
        kwargs={"orderID": orderID}
    ))