from django.shortcuts import render
from authentication.models import CustomUser
from django.core.paginator import Paginator
from userProfile.models import *




# [ DECORATORS ]
def restaurant_customer_homepage(request):

    # Make a query in the "CustomUser" model, to find all the restaurants.
    restaurants = CustomUser.objects.filter(
        is_restaurant_owner = True
    )

    # restaurant-profiles will be appended in this list
    rest_profile = []

    # print(restaurants.count())
    for rest in restaurants:
        # print(rest.restaurant_name)
        # querying the restaurant-profiles, then appending in the list ("rest_profile")
        rest_profile.append(RestaurantProfile.objects.get(user=rest.id))
    
    # print(rest_profile)
    for rProfile in rest_profile:
        print(rProfile.restaurant_profile_pic)



    restaurant_paginator = Paginator(restaurants, 5)
    restaurant_page = request.GET.get('page')
    paginated_restaurant_list_query = restaurant_paginator.get_page(restaurant_page)

    context = {
        'title': 'Restaurant Customer Homepage',
        'restaurants': paginated_restaurant_list_query,
        'rest_profile': rest_profile,
    }
    return render(request, 'restaurantCustomer/index.html', context)
