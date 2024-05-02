from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from food.models import *
from authentication.models import *
from django.urls.base import reverse





def lovedFoodList(request):
    # get the customer-instance from the "CustomUser" model
    customerInstance = CustomUser.objects.get(pk=request.user.id)
    print('Customer Instance (Food Liked List Page): ', customerInstance)

    # get all the food-liked-instance from the "FoodLikes" model
    foodLikeInstances = FoodLikes.objects.filter(customer_id=customerInstance).all()
    for fl in foodLikeInstances:
        print('Customer Food-Likes Instance (Food Liked List Page): ', fl.food_id)

    context = {
        'title': 'Loved List',
        'foodLikeInstances': foodLikeInstances,
    }
    return render(request, 'restaurantCustomer/loved_food_cust_view.html', context)








def removeLovedFood(request, lovedFoodID):
    print('LOved food ID remove page is called!')
    print('Loved Food ID: ', lovedFoodID)

    try:
        # get the loved-food-instance and then remove that instance
        lovedFoodInstance = FoodLikes.objects.get(pk=lovedFoodID)
        print('Loved Food Instance: ', lovedFoodInstance)
        print('Loved Food Instance Customer Name: ', lovedFoodInstance.customer_id)
        print('Loved Food Instance Food Name: ', lovedFoodInstance.food_id)

        lovedFoodInstance.delete()

    except:
        return HttpResponse ('The loved food instance is not found!')


    return redirect('restCustApp:lovedFoodList')
