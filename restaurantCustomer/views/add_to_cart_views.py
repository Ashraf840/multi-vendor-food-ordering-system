from django.shortcuts import render
from cartOrder.models import *
from django.shortcuts import redirect
from django.urls.base import reverse
from authentication.models import *



# [ Decorators ]
def foodCart(request, cartID):

    # print(cartID)
    # print( type(cartID) )

    cart = Cart.objects.get(cart_id=cartID)
    # print(cart)
    # print(cart.restaurant)

    # Get the restaurant-id from the "CustomUser" db-model
    restaurant = CustomUser.objects.get(restaurant_name=cart.restaurant)
    # print('*'*10)
    # print(restaurant)
    # print(restaurant.id)
    # print('*'*10)

    # Include 2% VAT for using this service
    totalVAT = ((cart.total_price * 2) / 100)
    cartPriceVAT = cart.total_price + totalVAT
    print('x'*10)
    print('Cart VAT: %s' % totalVAT)
    print('Cart (Incl. VAT): %s' % cartPriceVAT)
    print('x'*10)

    deliveryCharge = 15
    cartPrice_Include_DeliveryCharge_VAT = cart.total_price + deliveryCharge + totalVAT
    print('Cart total price: %s' % cart.total_price)
    print('Cart Price after including delivery charge & VAT: %s' % cartPrice_Include_DeliveryCharge_VAT)
    
    # [ Important Note ] To make a query to a db-model based on a foreignKey, 
    # then the FK needs to be queried from the origin db-model. then INSTANCE needs to stored inside a variable, then the variable will be set in the query-field of another db-model, where its working as a foreignKey.
    # cause django-ORM requires an instance of the foreignKey element if any FK exists in a db-model.
    # This also applied in terms of "create()" query.
    cartItems = CartItem.objects.filter(cart_id=cart)
    # print(cartItems)

    context = {
        'title': 'Food Order Cart',
        'cart': cart.customer,
        'cartID': cartID,
        'cartItems': cartItems,
        'restaurant': restaurant,
        'cartTotalPrice': cart.total_price,
        'totalVAT': totalVAT,
        'deliveryCharge': deliveryCharge,
        'cartPriceDeliveryChargeVAT': cartPrice_Include_DeliveryCharge_VAT,
    }
    # redirecting to the same food-detail page after updating food-information using the browser's url
    # https://stackoverflow.com/questions/57077059/how-do-i-redirect-to-the-same-page-after-an-action-in-django
    # return HttpResponseRedirect(request.path_info)
    # return redirect(request.path)
    # return HttpResponseRedirect(reverse('restCustApp:rest_page_cust_view'))
    return render(request, 'restaurantCustomer/add_to_cart.html', context)






# [ Decorators ]
def removeCartItem(request, cartItemId):
    # print(cartItemId)

    cartItem = CartItem.objects.get(cartItem_id=cartItemId)
    # print('*'*10)
    # print(cartItem)
    # print(cartItem.cart_id)
    # print(cartItem.quantity)
    # print(cartItem.price)
    # print('*'*10)

    cart = cartItem.cart_id
    

    # Get inside the instacne of the "Cart" model
    # Then update the total-item-quantity & total-price of the cart instacne
    cartModel = Cart.objects.get(cart_id=cartItem.cart_id)

    # print('x'*10)
    # print('Cart Model (ID): %s' % cartModel)
    # print('Cart Total Items: %s' % cartModel.total_cart_items)
    # print('Cart Total Price: %s' % cartModel.total_price)


    # [ I M P O R T A N T ]: updates the corresponding cart instance's total-item-quantity & total-price
    # [ OK - updates the cart's total-items-quantity & total-price ]
    cartModel.total_cart_items -= 1
    cartModel.total_price -= cartItem.price
    cartModel.save()
    
    
    # print('[*After updating the quantity & price*]')
    # print('Cart Total Items: %s' % cartModel.total_cart_items)
    # print('Cart Total Price: %s' % cartModel.total_price)
    # print('x'*10)


    if cartItem:
        cartItem.delete()
    
    
    # [ Further Development ] not working; if not cart-item exist, then redirect the customer to the homepage
    # if cartItem is None:
    #     return redirect('restCustApp:rcust_homepage')


    # [ Passing Args/ Params along with the "return redirect" function ]
    # [ Ref Link ]:  https://stackoverflow.com/a/47731223
    # [ Explanation ] The "cartID" is required to the "foodCart" page in order to make the query to find all the cart-items from the the "CartItem" db-model using the cartID.
    return redirect(reverse(
            'restCustApp:foodCart', 
            kwargs={"cartID": cart}
    ))



