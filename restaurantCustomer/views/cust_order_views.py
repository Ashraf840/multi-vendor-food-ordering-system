from django.shortcuts import render
from cartOrder.models import *
from authentication.models import CustomUser
from django.db.models import Q  # to make complex queries, if not found, throws an exceptionError
# from restaurantCustomer.forms import *
from django.shortcuts import redirect
from django.urls.base import reverse
from django.http import HttpResponse




"""
*********** Right-side foodOrder will be in the "cartOrder" application's views/ methods ***********
So the "confirm-order", "cancel-order" function is in the "cartOrder" application.
"""


def customer_order(request, cartID):
    # print('Request: ', request)
    # print('User: ', request.user)
    # print('User Email: ', request.user.email)
    # print('Cart ID: ', cartID)

    # Get the cart instance, will be used querying in the "Order" model
    # the cart-id is required to be passed in the page, cause the (delivery-handle, ) requires the cart-id since the handle-views uses the "reverse" method to redirect to this "customer_order" view.
    cart = Cart.objects.get(cart_id=cartID)
    # print('Cart Instance: ', cart)
    # print('Cart Total Price: ', cart.total_price)

    # Get the customer instance, will be used querying in the "Order" model
    customer = CustomUser.objects.get(email=request.user.email)
    # print('Customer Instance: ', customer)



    # [ Important Function ]
    # Make a query in the "Order" model to find the order-data.
    # If order data doesn't exist, create a new order-data for the customer corresponding to that cart.
    try:
        # Get the order-info corresponding the latest cart based on the corresponding customer.
        # Will execute the "except" block if no order-instance is found.
        custOrder = Order.objects.get(
            Q(customer=customer)
            & Q(cart_id=cart)
        )
        # print('Order Info: ', custOrder)

        # get all the cart-items corresponding to that specific customer-cart.
        cartItems = CartItem.objects.filter(cart_id=cart)
        
        # for critem in cartItems:
        #     print(critem.food)

        # restaurant = cart.restaurant
        # print('Restaurant: ', restaurant)
        # print('Restaurant: ', cart.restaurant)

        # [ Calculation of the food-order-price ]
        # Include 2% VAT for using this service
        totalVAT = ((cart.total_price * 2) / 100)
        cartPriceVAT = cart.total_price + totalVAT
        deliveryCharge = 15
        cartPrice_Include_DeliveryCharge_VAT = cart.total_price + deliveryCharge + totalVAT


        # Customer Personal Detail (from "CustomUser" model)
        # print('Customer Email: ', customer.email)
        # print('Customer First Name: ', customer.first_name)
        # print('Customer Last Name: ', customer.last_name)
        # print('Customer Phone: ', customer.phone)


        # deliveryDetailForm = OrderDeliveryDetailForm()
    except:
        print('No order data found! Need to create a new order instance based on the corresponding customer & cart')
        Order.objects.create(
            customer=customer
            ,cart_id=cart
            ,price=cart.total_price
            ,restaurant=cart.restaurant
        )
        print('Created a new order-data of this cart \'%s\' for this customer \'%s\'.' %  (cart, customer) )

        # Display an empty "PaymentMethodForm" form
        # PaymentForm = PaymentMethodForm()

        return redirect(reverse(
            'restCustApp:customerOrder', 
            kwargs={"cartID": cart}
        ))


    context = {
        'title': 'Customer Order',
        'custOrder': custOrder,
        'cart': cart,
        'cartItems': cartItems,
        'restaurant': cart.restaurant,
        'cartTotalPrice': cartPriceVAT,
        'deliveryCharge': deliveryCharge,
        'cartPriceDeliveryChargeVAT': cartPrice_Include_DeliveryCharge_VAT,
        'customer': customer,
        # 'deliveryDetailForm': deliveryDetailForm,
    }
    return render(request, 'restaurantCustomer/cust_order.html', context)







# Create another view to handle the POST.req sends from the delivery-details form.
# After updating the order-instance accordingly to the delivery-time & delivery-address, redirect the customer the corresponding order-page using "reverse" method

def deliveryDetail(request, cartID):
    if request.method == 'POST':
        print('Delivery Detail is being handled!')
        # print('Request: ', request)
        # print('User: ', request.user)
        # print('User Email: ', request.user.email)
        # print('Cart ID: ', cartID)

        deliveryTime = request.POST['deliveryTime']
        deliveryAddress = request.POST['deliveryAddress']
        # print('Delivery TIme: ', deliveryTime)
        # print('Delivery Address: ', deliveryAddress)


        # Get the instance of the corresponding customer using the customer-email
        customer = CustomUser.objects.get(email=request.user.email)
        # print('Customer Instance: ', customer)
        
        # Get the instance of the corresponding cart
        cart = Cart.objects.get(cart_id=cartID)
        # print('Cart Instance: ', cart)
        # Get the order instance corresponding to both the customer & the cart


        # If order data doesn't exist, create a new order-data for the customer corresponding to that cart.
        try:
            # Get the order-info corresponding the latest cart based on the corresponding customer.
            # Will execute the "except" block if no order-instance is found.
            custOrder = Order.objects.get(
                Q(customer=customer)
                & Q(cart_id=cart)
            )
            print('Order Info: ', custOrder)

            # [ Note ]: delivery-address & order-time of the "order" instance will be handled here.
            # [ Important ]: updateing the delivery-address & delivery-time of the order-instance
            custOrder.delivery_address = deliveryAddress
            custOrder.delivery_time = deliveryTime
            custOrder.save()
        except:
            print('No order data is found! Redirecting the customer to the shopping cart page, so that a new order-instance can be generated while the customer hit for order-checkout again!')
            # redirect to the customer-food-cart if if is not found, so that a new order can be created by clicking on the 'checkout' btn inside the food-cart page.
            return redirect(reverse(
                'restCustApp:foodCart', 
                kwargs={"cartID": cartID}
            ))

        # redirect to the customer-order page after handling the delivery address.
        return redirect(reverse(
            'restCustApp:customerOrder', 
            kwargs={"cartID": cartID}
        ))
    else:
        return HttpResponse('Not a POST method! Delivery detail is not updated of this order instance!')




def personalDetail(request, customerID, cartID):
    # [ Important Note ]:  "cartID" is used to redirect to the exact customer-order page
    # [ Important Note ]:  "customerID" is used to make query in the "CustomUser" db-model
    if request.method == 'POST':
        print('x'*10)
        print('Personal Detail is called!')
        print('x'*10)
        # print('Customer ID: ', customerID)
        # print('Cart ID: ', cartID)


        # Get the request.POST data from the "Personal Detail" form.
        custEmail = request.POST['email']
        custFirstName = request.POST['firstName']
        custLastName = request.POST['lastName']
        custPhone = request.POST['phoneNumber_DBvalue']

        # print('Customer Email: ', custEmail)
        # print('Customer First Name: ', custFirstName)
        # print('Customer Last Name: ', custLastName)
        # print('Customer Phone: ', custPhone)

        # Update the customer-instace of the "CustomUser" db-model
        customer = CustomUser.objects.get(id=customerID)
        print('Customer Instance: ', customer)

        customer.email=custEmail
        customer.first_name=custFirstName
        customer.last_name=custLastName
        customer.phone=custPhone
        customer.save()

        print('Customer Email: ', custEmail)
        print('Customer First Name: ', custFirstName)
        print('Customer Last Name: ', custLastName)
        print('Customer Phone: ', custPhone)


        return redirect(reverse(
            'restCustApp:customerOrder', 
            kwargs={"cartID": cartID}
        ))





def paymentMethodCOD(request, orderID, cartID):
    if request.method == 'POST':
        print('x'*10)
        print('Payment Method (COD) is called!')
        print('x'*10)

        # Get the order-id and change the payment-method of that order-instance
        # If order data doesn't exist, create a new order-data for the customer corresponding to that cart.
        try:
            # Get the order-info corresponding the latest cart based on the corresponding order-id.
            # Will execute the "except" block if no order-instance is found.
            custOrder = Order.objects.get(
                Q(order_id=orderID)
            )
            print('Order Info: ', custOrder)

            # [ Note ]: payment-method of the "order" instance will be handled here.
            # [ Important ]: updating the payment-method of the order-instance
            custOrder.payment_method = 'COD'
            custOrder.save()
        except:
            print('No order data is found! Redirecting the customer to the shopping cart page, so that a new order-instance can be generated while the customer hits for order-checkout again!')
            # redirect the customer to the customer-food-cart if the order is not found, so that a new order can be created by the customer clicking on the 'checkout' btn inside the food-cart page.
            return redirect(reverse(
                'restCustApp:foodCart', 
                kwargs={"cartID": cartID}
            ))

        # After executing the 'try' block, this following redirection will be executed.
        return redirect(reverse(
            'restCustApp:customerOrder', 
            kwargs={"cartID": cartID}
        ))
    else:
        return HttpResponse('Not a POST method! Payment method is not updated of this order instance!')








def paymentMethodSSLCommerz(request, orderID, cartID):
    if request.method == 'POST':
        print('x'*10)
        print('Payment Method (SSLCommerz) is called!')
        print('x'*10)

        # Get the order-id and change the payment-method of that order-instance
        # If order data doesn't exist, create a new order-data for the customer corresponding to that cart.
        try:
            # Get the order-info corresponding the latest cart based on the corresponding order-id.
            # Will execute the "except" block if no order-instance is found.
            custOrder = Order.objects.get(
                Q(order_id=orderID)
            )
            print('Order Info: ', custOrder)

            # [ Note ]: payment-method of the "order" instance will be handled here.
            # [ Important ]: updating the payment-method of the order-instance
            custOrder.payment_method = 'SSLCommerz'
            custOrder.save()
        except:
            print('No order data is found! Redirecting the customer to the shopping cart page, so that a new order-instance can be generated while the customer hits for order-checkout again!')
            # redirect the customer to the customer-food-cart if the order is not found, so that a new order can be created by the customer clicking on the 'checkout' btn inside the food-cart page.
            return redirect(reverse(
                'restCustApp:foodCart', 
                kwargs={"cartID": cartID}
            ))

        # After executing the 'try' block, this following redirection will be executed.
        return redirect(reverse(
            'restCustApp:customerOrder', 
            kwargs={"cartID": cartID}
        ))
    else:
        return HttpResponse('Not a POST method! Payment method is not updated of this order instance!')
