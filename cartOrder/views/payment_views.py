from django.shortcuts import render
from django.http import HttpResponse
from cartOrder.models import *
from django.shortcuts import redirect
from django.urls.base import reverse






# # This method will generate a random-string of 20 chars.
# def random_string_generator(size=20, chars=string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))



# After the payment view, the customer will be redirect to the "Order Summarized" page, here the order-status will be changed in real-time using redis-server.
def payment(request, orderID, cartID):
    if request.method == 'POST':
        print('x'*10)
        print('Payment def is called!')
        print('Order ID: ', orderID)
        print('Cart ID: ', cartID)
        print('x'*10)

        print(request)

        # [ Note ]: get the post-request-values ('grandTotalPrice', 'payment') of the form
        orderGrandTotalPrice = request.POST['grandTotalPrice']  # need to add the deliveryFee + VAT into the "price" field of the "Order" db-model.
        orderPaymentMethod = request.POST['payment']    # need to check, if the method is SSLCommerz, then handle the process differently.

        print('Request - Order Grand Total Price: ', orderGrandTotalPrice)
        print('Request - Order Payment Method: ', orderPaymentMethod)


        # orderInstance = Order.objects.get(order_id=orderID)
        # print('Order Instance: ', orderInstance)

        print(request.user)
        print(random_string_generator())

        # Get the order-instance
        try:
            # Get the order-info corresponding the latest cart based on the corresponding customer.
            # Will execute the "except" block if no order-instance is found.
            orderInstance = Order.objects.get(order_id=orderID)
            orderInstance.price = orderGrandTotalPrice
            orderInstance.save()
            print('Order Instance: ', orderInstance)
            print('Order Number: ', orderInstance.order_num)

            # Handle the process accordinly based on the payment-method
            if orderPaymentMethod == 'COD':
                # Change the cart's order-status to True
                cartInstance = Cart.objects.get(cart_id=orderInstance.cart_id)
                print('Payment Method: COD')
                print('Cart Instance: %s' % cartInstance)

                cartInstance.is_ordered = True
                cartInstance.save()




            if orderPaymentMethod == 'SSLCommerz':
                print('Payment Method: SSLCommerz')




            return redirect(reverse(
                'restCustApp:customerOrderSummary', 
                kwargs={
                    "orderID": orderID
                    ,"cartID": cartID
                }
            ))
        except:
            print('No order data is found! Redirecting the customer to the shopping cart page, so that a new order-instance can be generated while the customer hits for "order-checkout" again!')
            # redirect to the customer-food-cart if if is not found, so that a new order can be created by clicking on the 'checkout' btn inside the food-cart page.
            return redirect(reverse(
                'restCustApp:foodCart', 
                kwargs={"cartID": cartID}
            ))

        # Get the cart-instance
        # cartInstance = Cart.objects.get(cart_id=orderInstance.cart_id)


        response = ('Order ID: %s %s Order Instance: %s %s Cart ID: %s' % (orderID, ('-'*10), orderInstance, ('-'*10), cartID))
        return HttpResponse(response)
