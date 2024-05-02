from django.shortcuts import render
from cartOrder.models import *
from django.shortcuts import redirect
from django.urls.base import reverse
from django.db.models import Q
from django.http import HttpResponse



# -----------------------------------------
# All URLs are in the "restaurantCustomer" application.
# -----------------------------------------



# After the payment view, the customer will be redirect to the "Order Summarized" page, here the order-status will be changed in real-time using redis-server.
def orderSummary(request, orderID, cartID):

    print('Cart ID: ', cartID)

    # Get the order instance
    try:
            # Get the order-info corresponding the latest cart based on the corresponding customer.
            # Will execute the "except" block if no order-instance is found.
            orderInstance = Order.objects.get(order_id=orderID)

            # get all the cart-items corresponding to that specific customer-cart.
            # get the cart-instance
            cart = Cart.objects.get(cart_id=cartID)
            print('Cart Instance: ', cart)

            # get the cartItem-instance
            cartItems = CartItem.objects.filter(cart_id=cart)
            # for cit in cartItems:
            #     print(cit)

            # [ Calculation of the food-order-price ]
            # Include 2% VAT for using this service
            totalVAT = ((cart.total_price * 2) / 100)
            cartPriceVAT = cart.total_price + totalVAT

    except:
        print('No order data is found! Redirecting the customer to the homepage, so that a new order-process can generated!')
        # redirect to the customer-food-cart if if is not found, so that a new order can be created by clicking on the 'checkout' btn inside the food-cart page.
        return redirect('restCustApp:rcust_homepage')


    context = {
        'title': 'Order Summary',
        'orderID': orderID,
        'cartID': cartID,
        'orderInstance': orderInstance,
        'cartItems': cartItems,
        'cartTotalPrice': cartPriceVAT,
    }
    return render(request, 'cartOrder/order_summary.html', context)






def cancelOrder(request, orderID, cartID):
    print('x'*10)
    print('Cancel order method is called!')
    print('Order ID: ', orderID)
    print('x'*10)

    if request.method == 'POST':
        try:
            # Get the order-instance & change the "is-cancelled" field from False to True
            orderInstance = Order.objects.get(order_id=orderID)
            orderInstance.is_cancelled = True
            orderInstance.save()
            print('Order Instance: ', orderInstance)
        except:
            response = ('Order is not found!')
            return HttpResponse(response)


    return redirect(reverse(
        'restCustApp:customerOrderSummary', 
        kwargs={
            "orderID": orderID
            ,"cartID": cartID
        }
    ))
