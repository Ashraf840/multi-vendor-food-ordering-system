from django.shortcuts import render
from cartOrder.models import *
from userProfile.models import RestaurantProfile
from authentication.models import CustomUser
from django.db.models import Q  # to make complex queries, if not found, throws an exceptionError
from food.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls.base import reverse
from restaurantCustomer.forms import *






# [ DECORATORS ]
def restaurant_page_cust_view(request, id):
    # Get the restaurant-information.
    print('Restaurant ID: ', id)
    restaurantInfo = CustomUser.objects.get(pk=id)
    # print(restaurantInfo)   # displays the restaurant-name
    # print(restaurantInfo.restaurant_name)   # displays the restaurant-name

    # Get the restaurant profile based on the data from the "CustomUser" model
    restaurantProfile = RestaurantProfile.objects.get(user=restaurantInfo)
    # print(restaurantProfile)
    # print(restaurantProfile.restaurant_profile_pic)

    # Make a query to fetch the food-category-names of the specific restaurant-owner-staff
    food = Food.objects.filter(
        Q(created_by=restaurantInfo)
    ).all()

    print('x'*10)
    print(food)
    print('x'*10)





    custInfo = request.user
    # print(custInfo)
    # get all the cart of the user. [ this comment will be deleted ]


    # [ Important Function ]: Check if a customer has any cart of different restaurant where there are items in it, before entering into a restaurant-page.
    # If so, delete that draft-cart of that restaurant, and then check if the customer has a cart for the current-restaurant, if no, then create a brand new cart.
    try:
        # Get the customer-info and the latest cart, where "is_ordered" is False.
        custCart = Cart.objects.filter(
            Q(customer=custInfo)
            & Q(is_ordered=False)
            # & Q(restaurant=restaurantInfo.restaurant_name)
        )
        # .latest('last_updated_at')  # [not necessary]

        print('*'*10)
        for cCart in custCart:
            print('Restaurant: %s; Cart-Item: %s' % (cCart.restaurant, cCart.total_cart_items))

            # Check if any cart has any item in it
            if cCart.total_cart_items > 0:
                # Check if the restaurant-name of the cart matches the currently-viewing restaurant-page's name, if not so, then delete that cart of the previous restaurant
                if cCart.restaurant != restaurantInfo.restaurant_name:
                    print('this cart \'%s\' needs to be deleted' % cCart.restaurant)
                    cCart.delete()
            
            # if cCart.restaurant != restaurantInfo.restaurant_name:
            #     print('Create a new cart of this restaurant %s for this customer' % restaurantInfo.restaurant_name)
        # print(custCart.restaurant)
        # print(custCart.total_cart_items)
        print('*'*10)



        # if no cart is found, create a new cart of the restaurant for the customer
        custCart_find_restaurant = Cart.objects.filter(
            customer=custInfo
            ,is_ordered=False
            ,restaurant=restaurantInfo.restaurant_name
        )
        # ******************************************************* [ Doesn't work if a cart gets deleted, & the customer reenter into the same restaurant-page ]
        # custCart_find_restaurant = Cart.objects.get(
        #     customer=custInfo
        #     ,is_ordered=False
        #     ,restaurant=restaurantInfo.restaurant_name
        # )
        # *******************************************************
        print(custCart_find_restaurant)
        # print(custCart_find_restaurant.restaurant)

        custCart_single = ''
        for ccfrst in custCart_find_restaurant:
            custCart_single = ccfrst

        # Create a new restaurant-cart for the customer
        if not custCart_find_restaurant:
            Cart.objects.create(
                customer=custInfo
                ,restaurant=restaurantInfo.restaurant_name
            )
            print('Created a new cart of this restaurant \'%s\' for this customer' % restaurantInfo.restaurant_name)



        # if custCart.total_cart_items > 0 and custCart.restaurant != restaurantInfo.restaurant_name:
        # if custCart.total_cart_items > 0:
        #     print('*'*10)
        #     print('the latest cart is deleted! Cause this draft cart has item(s) from another restaurant in it. & the customer is currently visiting anpther restaurant.')
        #     print('Now a fresh new cart needs to be created for this customer, which will be valid till this restaurant page!')
        #     print('*'*10)
        #     pass
        # else:
        #     print('You are in the same restaurant-page!')
    except:
        # No cart not found for this restaurant. So created a new cart for this customer; valid till this restaurant-page.
        # Cart.objects.create(
        #     customer=custInfo
        #     , restaurant=restaurantInfo.restaurant_name
        # )
        print('No cart not found for this restaurant %s' % restaurantInfo.restaurant_name)
        print('So created a new cart for this customer; Restaurant: %s!' % restaurantInfo.restaurant_name)





    # [ not using this block, akready completed above ]
    # try:
    #     # Get the cart of the user for the [current restaurant],
    #     custCart = Cart.objects.filter(
    #         Q(customer=custInfo)
    #         & Q(is_ordered=False)
    #         & Q(restaurant=restaurantInfo.restaurant_name)
    #     ).latest('last_updated_at')

    #     print('Cart found')
    #     print(custCart.last_updated_at)
    #     print(custCart.restaurant)

    #     # # check if its from another restaurant, 
    #     # # then delete the cart & create a fresh-new cart for the user.
    #     # # [ Further Devleopment ] if the cart-item is greater than 0, then delete the cart and re-create the cart.
    #     # # and the restaurant-name is ddifferent than the current-request.
    #     if custCart.total_cart_items > 0 and custCart.restaurant != restaurantInfo.restaurant_name:
    #         # print(custCart.total_cart_items)
    #         print('this cart needs to be deleted. Cause it contains items of different restaurant')
    #         # custCart.delete()
    #         # print('the latest cart is deleted! Cause this cart has item(s) from another restaurant in it.')
    #         # Cart.objects.create(
    #         #     customer=custInfo
    #         #     , restaurant=restaurantInfo.restaurant_name
    #         # )
    #         # print('So created a new fresh cart for the customer! Restaurant: %s!' % restaurantInfo.restaurant_name)
    #         pass
    # except:
    #     # Create a fresh-new cart for the customer
    #     Cart.objects.create(
    #         customer=custInfo
    #         , restaurant=restaurantInfo.restaurant_name
    #     )
    #     # print('created a new cart for the customer; Restaurant: %s!' % restaurantInfo.restaurant_name)
    #     print('Cart not found')
    #     pass









    # custCart = Cart.objects.filter(
    #     Q(customer=custInfo)
    #     & Q(is_ordered=False)
    # ).latest('last_updated_at')
    # print(custCart.total_cart_items)

    
    # if the cart-item is greater than 0, then delete the cart and re-create the cart.
    # and the restaurant-name is ddifferent than the current-request.
    # if 
        # if custCart.total_cart_items > 0:
        #     custCart.delete()
        #     print('the latest cart is deleted!')

        #     # Create a new cart for the user
        #     # Cart.objects.create(
        #     #     customer=
        #     # )
        #     pass

    # print(request.path_info)

    form = AddtoCartForm()

    context = {
        'title': 'Restaurant Page',
        'rest_id': id,

        # restaurant info-obj fetched from "CustomUser" model
        'restaurantInfo': restaurantInfo,
        # restaurant info-obj fetched from "CustomUser" model
        'r_profile': restaurantProfile,
        # Fetch all the food of this restaurant
        'food': food,
        # 'custCart': custCart_find_restaurant,
        # 'custCart': custCart_find_restaurant,
        'custCart': custCart_single,
        'form': form,
    }
    return render(request, 'restaurantCustomer/restaurant_page_cust_view.html', context)








# [ Decorators ]
# def addToCart(request, cart, customer, food):
def addToCart(request):
    print('*'*20)
    print(request)
    print('*'*20)
    # print(cart)
    # print(customer)
    # print(food)

    # CartItem.objects.create(
    #     cart=cart
    #     # ,customer=customer
    #     ,food=food
    # )

    # if request.method == 'POST':
    #     form = AddtoCartForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('restCustApp:addToCart')    # redirect to the homapage




    # [ Further Development ]: store the cart value in the sesion, so that it can be used for hitting the food-cart page
    # request.session['cart'] = 
    # cartGblScope = ''

    if request.method == 'POST':
        cart = request.POST['cart']
        food = request.POST['food']
        quantity = int(request.POST['quantity'])

        # cartGblScope = cart

        # print('*'*10)
        # print('Cart: %s ----------- Type: %s' % ( cart, type(cart) ))
        # print('Food: %s ----------- Type: %s' % ( food, type(food) ))
        # print('Quantity: %s ----------- Type: %s' % ( quantity, type(quantity) ))
        # print('*'*10)


        # [ Important Note ] Since the "CartItem" model contains foreign-keys ("cart_id", "food"), so they cannont be entered directly inserted into the "CartItem" model using the  "CartItem.objects.create()" query.
        # Thus they first needs to be fetched from their origin-db-model, then they can be inserted using the "create()" query.
        cartInstance = Cart.objects.get(cart_id=cart)
        foodInstance = Food.objects.get(food_name=food)

        CartItem.objects.create(
            cart_id=cartInstance
            ,food=foodInstance
            ,quantity=quantity
        )

        # [ Passing Args/ Params along with the "return redirect" function ]
        # [ Ref Link ]:  https://stackoverflow.com/a/47731223
        # [ Explanation ] The "cartID" is required to the "foodCart" page in order to make the query to find all the cart-items from the the "CartItem" db-model using the cartID.
        return redirect(reverse(
            'restCustApp:foodCart', 
            kwargs={"cartID": cart}
        ))

    # else:
    #     # return redirect('restCustApp:rcust_homepage')
    #     return redirect(reverse(
    #         'restCustApp:foodCart', 
    #         kwargs={"cartID": cartGblScope}
    #     ))





    # context = {
    #     'title': 'Order Cart',
    # }
    # # redirecting to the same food-detail page after updating food-information using the browser's url
    # # https://stackoverflow.com/questions/57077059/how-do-i-redirect-to-the-same-page-after-an-action-in-django
    # # return HttpResponseRedirect(request.path_info)
    # # return redirect(request.path)
    # # return HttpResponseRedirect(reverse('restCustApp:rest_page_cust_view'))
    # return render(request, 'restaurantCustomer/add_to_cart.html', context)






# [ Decorators ]
# def foodCart(request, cartID):

#     # print(cartID)
#     # print( type(cartID) )

#     cart = Cart.objects.get(cart_id=cartID)
#     # print(cart)
    
#     # [ Important Note ] To make a query to a db-model based on a foreignKey, 
#     # then the FK needs to be queried from the origin db-model. then INSTANCE needs to stored inside a variable, then the variable will be set in the query-field of another db-model, where its working as a foreignKey.
#     # cause django-ORM requires an instance of the foreignKey element if any FK exists in a db-model.
#     # This also applied in terms of "create()" query.
#     cartItems = CartItem.objects.filter(cart_id=cart)
#     # print(cartItems)

#     context = {
#         'title': 'Food Order Cart',
#         'cartID': cartID,
#         'cartItems': cartItems,
#     }
#     # redirecting to the same food-detail page after updating food-information using the browser's url
#     # https://stackoverflow.com/questions/57077059/how-do-i-redirect-to-the-same-page-after-an-action-in-django
#     # return HttpResponseRedirect(request.path_info)
#     # return redirect(request.path)
#     # return HttpResponseRedirect(reverse('restCustApp:rest_page_cust_view'))
#     return render(request, 'restaurantCustomer/add_to_cart.html', context)




