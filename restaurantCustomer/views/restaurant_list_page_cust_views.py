from django.shortcuts import render
from authentication.models import CustomUser
from django.core.paginator import Paginator
from userProfile.models import *




def restaurant_list_cust_view(request):

    # get all the restaurants from the 'CustomUser' model
    restaurants = CustomUser.objects.filter(
        is_restaurant_owner = True
    ).all()

    for r in restaurants:
        print('Restaurant: ', r)

    total_restaurant_num = len(restaurants)

    context = {
        'title': 'Restaurant List',
        'restaurants': restaurants,
        'total_restaurant_num': total_restaurant_num,
    }
    return render(request, 'restaurantCustomer/restaurant_list_page_cust_view.html', context)

