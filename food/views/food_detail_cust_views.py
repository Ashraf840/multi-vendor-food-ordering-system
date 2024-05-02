from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from food.models import *
from django.db.models import Q  # to make complex queries
from django.urls.base import reverse
from cartOrder.models import *




def foodDetail(request, foodID, cartID):
    print('Food Detail Page is called!')
    print('Food ID: ', foodID)
    print('Cart ID: ', cartID)

    # get the food-nstance from the "Food" model
    foodInstance = Food.objects.get(pk=foodID)
    print('Food Instance: ', foodInstance)
    print('Restaurant ID (from "CustomUser" model): ', foodInstance.created_by.pk)


    # [ will be implemented in the customer-end, while he/ she views the food in it's detail page ]
    # check if the user is a regular user/ customer
    # **************** Total Views Increment ****************
    foodInstance.total_viewed += 1 
    foodInstance.save()
    # **************** Total Views Increment ****************
    

    # get the "FoodRating" instance from the "food" application
    try:
        # foodRatingInstance = FoodRating.objects.get(food_id=foodInstance.pk)
        
        # -----------------------------------------
        # Make queryset of the food-rating of this particular food
        food_rating = FoodRating.objects.filter(
            Q(food_id=foodInstance)
        ).all()

        signL = '*' * 10
        signR = '*' * 10
        print('%s Food Rating: %s %s' % (signL, food_rating, signR))


        # Average Rating Calculation
        # Equation (method-1):   AR = (1*a + 2*b + 3*c + 4*d + 5*e) / totalQuantityOfRating
        # Equation (method-1):   AR = (ratings += ratings) / totalQuantityOfRating
        totalRatingQuantity_counter = 0
        totalRating = 0
        
        AvgRating = 0

        # The following variables will be used for demonstrating the ratings individually
        rating_1_counter = 0
        rating_2_counter = 0
        rating_3_counter = 0
        rating_4_counter = 0
        rating_5_counter = 0
        
        for ratings in food_rating:
            totalRatingQuantity_counter += 1
            totalRating += ratings.rating
            # print(ratings.rating)

            # Used to demonstrate separately
            if ratings.rating == 1:
                rating_1_counter += 1
            elif ratings.rating == 2:
                rating_2_counter += 1
            elif ratings.rating == 3:
                rating_3_counter += 1
            elif ratings.rating == 4:
                rating_4_counter += 1
            elif ratings.rating == 5:
                rating_5_counter += 1
            else:
                pass

            
        print('Total Rating Counter: %s' % totalRatingQuantity_counter)
        print('Total Rating: %s' % totalRating)
        try:
            avgRating = totalRating / totalRatingQuantity_counter
        except:
            avgRating = 0
        print('Average Rating: %s' % avgRating)

        print('Total Ratings for 1: %s' % rating_1_counter)
        print('Total Ratings for 2: %s' % rating_2_counter)
        print('Total Ratings for 3: %s' % rating_3_counter)
        print('Total Ratings for 4: %s' % rating_4_counter)
        print('Total Ratings for 5: %s' % rating_5_counter)

        try:
            avgRating_for_1 = (rating_1_counter * 100) / totalRatingQuantity_counter
        except:
            avgRating_for_1 = 0

        try:
            avgRating_for_2 = (rating_2_counter * 100) / totalRatingQuantity_counter
        except:
            avgRating_for_2 = 0

        try:
            avgRating_for_3 = (rating_3_counter * 100) / totalRatingQuantity_counter
        except:
            avgRating_for_3 = 0

        try:
            avgRating_for_4 = (rating_4_counter * 100) / totalRatingQuantity_counter
        except:
            avgRating_for_4 = 0

        try:
            avgRating_for_5 = (rating_5_counter * 100) / totalRatingQuantity_counter
        except:
            avgRating_for_5 = 0


        print('Average Ratings for 1: %s' % avgRating_for_1)
        print('Average Ratings for 2: %s' % avgRating_for_2)
        print('Average Ratings for 3: %s' % avgRating_for_3)
        print('Average Ratings for 4: %s' % avgRating_for_4)
        print('Average Ratings for 5: %s' % avgRating_for_5)
        # -----------------------------------------

        # get the customer-instance from "CustomUser" db-model
        print('Customer: ', request.user)
        print('Customer: ', request.user.id)
        customerInstance = CustomUser.objects.get(pk=request.user.id)
        print('Customer Instance: ', customerInstance)
        
        # get the food-rating-instance, if no rating is done, then create a new food-rating for that specific customer for that food.
        try:
            custFoodRatingInstance = FoodRating.objects.get(
                Q(customer_id=customerInstance)
                & Q(food_id=foodInstance)
            )
            print('Customer Food Rating Instance: ', custFoodRatingInstance)
        except:
            custFoodRatingInstance = FoodRating.objects.create(
                customer_id=customerInstance
                ,food_id=foodInstance
                ,rating=0
            )
            print('Create a New Food Rating Instance (w/ rating 0): ', custFoodRatingInstance)



        # # get the customer-info
        # custInfo = request.user
        # print('Customer ID: ', custInfo)

        # # # get customer-instance
        # customerInstance = CustomUser.objects.get(pk=custInfo.pk)

        # # # Get the customer-info and the latest cart, where "is_ordered" is False.
        # custCart = Cart.objects.filter(
        #     Q(cart_id=cartID)
        # )
        # print('Csutomer Cart Instance: ', custCart)
        # print('Csutomer Cart Instance ID: ', custCart.cart_id)

        # # # if no cart is found, create a new cart of the restaurant for the customer
        # # custCart_find_restaurant = Cart.objects.filter(
        # #     customer=custInfo
        # #     ,is_ordered=False
        # #     ,restaurant=restaurantInfo.restaurant_name
        # # )


        try:
            foodLieksInstance = FoodLikes.objects.get(
                Q(customer_id = customerInstance)
                & Q(food_id = foodInstance)
            )
        except:
            print('No food likes is available!')
            foodLieksInstance = FoodLikes.objects.create(
                customer_id=customerInstance
                ,food_id=foodInstance
            )
            print('Create a New Food Like Instance (w/ like "Flase"): ', foodLieksInstance)
            foodLieksInstance = False


    except:
        print('No food rating is available!')
        food_rating = 0
        custFoodRatingInstance = 0


    context = {
        'title': 'Food Detail Page',
        'foodInstance': foodInstance,
        # 'foodRatingInstance': foodRatingInstance,
        'avgRating': avgRating,
        'custFoodRatingInstance': custFoodRatingInstance,
        'custCart': cartID,
        'foodLieksInstance': foodLieksInstance,

        # Total ratings of individual nums are used to display along with the progress-bar in the right-side
        'rating_1_counter': rating_1_counter,
        'rating_2_counter': rating_2_counter,
        'rating_3_counter': rating_3_counter,
        'rating_4_counter': rating_4_counter,
        'rating_5_counter': rating_5_counter,

        # Average rating of individual nums are used in the 'width' of the progress-bar
        'avgRating_for_1': avgRating_for_1,
        'avgRating_for_2': avgRating_for_2,
        'avgRating_for_3': avgRating_for_3,
        'avgRating_for_4': avgRating_for_4,
        'avgRating_for_5': avgRating_for_5,
    }
    return render(request, 'food/food_detail_cust_views.html', context)





# Method: Food Rating Update by Customer
def updateFoodRating(request, foodID, cartID):
    if request.method == 'POST':
        print('Food Rating Change Method for customer is called!')
        print('Food ID: ', foodID)
        print('Food ID: ', cartID)

        # get the value from the rating-slider
        reatingSliderValue = request.POST['foodRatingSlider']
        print('Rating slider Value: ', reatingSliderValue)

        try:
            # get the food-instance from the "Food" models
            foodInstance = Food.objects.get(pk=foodID)
            print('Food Instance: ', foodInstance)

            # get the foodRating-instance from the "FoodRating" model
            foodRatingInstance = FoodRating.objects.get(food_id=foodInstance.pk)
            print('Food Rating Instance: ', foodRatingInstance)

            # Update the food-rating value of this specific food-rating-instance
            foodRatingInstance.rating = reatingSliderValue
            foodRatingInstance.save()

            
            # [ Passing Args/ Params along with the "return redirect" function ]
            # [ Ref Link ]:  https://stackoverflow.com/a/47731223
            # [ Explanation ] The "cartID" is required to the "foodCart" page in order to make the query to find all the cart-items from the the "CartItem" db-model using the cartID.
            return redirect(reverse(
                'foodApp:food_detail', 
                kwargs={
                    "foodID": foodID
                    ,"cartID": cartID
                }
            ))

        except:
            return HttpResponse('Something went wrong!')

        
    else:
        return redirect(reverse(
            'foodApp:food_detail', 
            kwargs={
                "foodID": foodID
                ,"cartID": cartID
            }
        ))





def foodLiked(request, foodID, cartID):
    try:
        # get food-instance from "Food" model
        foodInstance = Food.objects.get(pk=foodID)
        print('Food Instance (Food Liked): ', foodInstance)

        # get customer instance from "CustomUser" model
        customerInstance = CustomUser.objects.get(pk=request.user.id)
        print('Customer Instance (Food Liked): ', customerInstance)

        # foodInstance.is_liked = True
        # foodInstance.save()

        try:
            foodLieksInstance = FoodLikes.objects.get(
                Q(customer_id = customerInstance)
                & Q(food_id = foodInstance)
            )

            foodLieksInstance.is_liked = True
            foodLieksInstance.save()

            return redirect(reverse(
                'foodApp:food_detail', 
                kwargs={
                    "foodID": foodID
                    ,"cartID": cartID
                }
            ))

        except:
            FoodLikes.objects.create(
                customer_id = customerInstance
                ,food_id = foodInstance
                ,is_liked = True
            )

            return redirect(reverse(
                'foodApp:food_detail', 
                kwargs={
                    "foodID": foodID
                    ,"cartID": cartID
                }
            ))

    except:
        return HttpResponse('Something went wrong!')







def foodUnliked(request, foodID, cartID):
    try:
        # get food-instance from "Food" model
        foodInstance = Food.objects.get(pk=foodID)
        print('Food Instance (Food Liked): ', foodInstance)

        # get customer instance from "CustomUser" model
        customerInstance = CustomUser.objects.get(pk=request.user.id)
        print('Customer Instance (Food Liked): ', customerInstance)

        # foodInstance.is_liked = True
        # foodInstance.save()

        try:
            foodLieksInstance = FoodLikes.objects.get(
                Q(customer_id = customerInstance)
                & Q(food_id = foodInstance)
            )

            foodLieksInstance.is_liked = False
            foodLieksInstance.save()

            return redirect(reverse(
                'foodApp:food_detail', 
                kwargs={
                    "foodID": foodID
                    ,"cartID": cartID
                }
            ))

        except:
            FoodLikes.objects.create(
                customer_id = customerInstance
                ,food_id = foodInstance
                ,is_liked = True
            )

            return redirect(reverse(
                'foodApp:food_detail', 
                kwargs={
                    "foodID": foodID
                    ,"cartID": cartID
                }
            ))

    except:
        return HttpResponse('Something went wrong!')



