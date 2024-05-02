from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.helper_functions.export_user_profile import export_user_profile
from food.models import *
from django.db.models import Q  # to make complex queries
from food.forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls.base import reverse
# from food.views.helper_functions.food_tag_insert import food_tag_insert as fti
from datetime import datetime as dt
from django.contrib.auth.decorators import login_required
from authentication.decorators import *





# Food List
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodList(request):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user-type, which will be displayed as the center-top panel of the page.
    user_type = get_user_type(userInfo)

    # [ HELPER FUNCTION ]: to grab the user-profile-data.
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    u_profile = export_user_profile(userID = u_id)

    # Make a query to fetch the food-category-names of the specific restaurant-owner-staff
    food = Food.objects.filter(
        Q(created_by=u_id)
    ).all()

    print(food)

    context = {
        'title': 'Food List',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,
        'food': food,
    }
    return render(request, 'food/food_list.html', context)






# Food List (Recently Added)
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodList_recentlyadded(request):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user-type, which will be displayed as the center-top panel of the page.
    user_type = get_user_type(userInfo)

    # [ HELPER FUNCTION ]: to grab the user-profile-data.
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    u_profile = export_user_profile(userID = u_id)


    # Make a query to find all the recelty added foods.
    # Get the current month of the year
    currentMonth = dt.now().month
    
    food = Food.objects.filter(
        Q(created_by=u_id) &
        Q(created_at__month=currentMonth)
    ).all()

    print('-' * 20)
    for f in food:
        print(f.food_name)
    print('-' * 20)

    context = {
        'title': 'Recently Added Food List',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,
        'food': food,
    }

    return render(request, 'food/recently_added_food_list.html', context)






# Create new food record
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def createFood(request):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user-type, which will be displayed as the center-top panel of the page.
    user_type = get_user_type(userInfo)

    # [ HELPER FUNCTION ]: to grab the user-profile-data.
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    u_profile = export_user_profile(userID = u_id)

    # Make the query to fetch all the Category-data.
    food_category = Category.objects.all()

    # print(food_category)
    for fc in food_category:
        print(fc.id)

    # Render the empty form of "Food"
    form = FoodForm()

    # POST request handling section: to create new food
    # [ Check if the same food from the same category is created previously ]
    if request.method == 'POST':
        # print(request.POST)
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            # print('form is valid')

            food_name = form.cleaned_data['food_name']     # fetched from "name" attr from the frontend.
            food_cate = form.cleaned_data['category']
            food_reward_point = form.cleaned_data['reward_point']
            food_price = form.cleaned_data['price']
            food_tag = form.cleaned_data['tag']
            food_addon = form.cleaned_data['addon']
            food_image = form.cleaned_data['image']

            print('Food Name (sent from the frontend form): %s' % food_name)
            print('Food Category (sent from the frontend form): %s' % food_cate)
            print('Food Reward Point (sent from the frontend form): %s' % food_reward_point)
            print('Food Price (sent from the frontend form): %s' % food_price)
            print('Food Tag (sent from the frontend form): %s' % food_tag)
            print('Food Addon (sent from the frontend form): %s' % food_addon)


            # Create new food record, without using the form
            # [ Further Development ]: Check if the restaurant-owner has the duplicate food record in the DB
            food_instance = Food.objects.create(
                food_name=food_name,
                category=food_cate,
                created_by=userInfo,
                reward_point=food_reward_point,
                price=food_price,
                # tag=food_tag,
                # addon=food_addon,
                image=food_image,
            )

            # To handle tthe many-to-many fields ("tag" & "addon")
            # [ Helper Ref Link ]:  https://stackoverflow.com/questions/50015204/direct-assignment-to-the-forward-side-of-a-many-to-many-set-is-prohibited-use-e
            food_instance.tag.set(food_tag)
            food_instance.addon.set(food_addon)


            messages.info(request, 'New Food Record Created: "%s"!' % food_name)
            return HttpResponseRedirect(reverse('foodApp:food_foodList'))

    context = {
        'title': 'Create Food Record',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,
        'form': form,
        'food_category': food_category,
    }
    return render(request, 'food/create_food_record.html', context)





# ********************************* Food-Detail View-func
# If any regular_user / customer hits this view-func, then increment the total_view_counter & also update the to the DB
# *********************************


# Update/ Modify Particular Food Item
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def updateDetailFood(request, id):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user-type, which will be displayed as the center-top panel of the page.
    user_type = get_user_type(userInfo)

    # [ HELPER FUNCTION ]: to grab the user-profile-data.
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    u_profile = export_user_profile(userID = u_id)

    # Make a query to fetch the food-record of the specific restaurant-owner-staff
    food_record = Food.objects.get(pk=id)

    
    
    # [ will be implemented in the customer-end, while he/ she views the food in it's detail page ]
    # check if the user is a regular user/ customer
    # **************** Total Views Increment ****************
    # food_record.total_viewed += 1 
    # food_record.save()
    # **************** Total Views Increment ****************



    # Initialize all the necessary forms with information regarding that particulat food (FoodForm, FoodImageForm, FoodTagForm, FoodAddonForm)
    form = FoodForm(instance=food_record)
    foodImageForm = FoodImageForm(instance=food_record)
    foodTagForm = TagForm()     # this empty tag-form will be rendered for the tag-insertion-modal

    # Make queryset of the food-rating of this particular food
    food_rating = FoodRating.objects.filter(
        Q(food_id=food_record)
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
    
    # Rating = 0
    # Rating = totalRating

    # Calculate the average rating of the particular food
    # AvgRating = (1*rating_1_counter + 2*rating_2_counter + 3*rating_3_counter + 4*rating_4_counter + 5*rating_5_counter) / totalRatingQuantity_counter
    # print('Average Rating: %s' % AvgRating)



    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food_record)   # REQUIRED since an image is also getting uploaded using this form; instance will only update that specific record
        foodImageForm = FoodImageForm(request.POST, request.FILES, instance=food_record)   # REQUIRED since an image is also getting uploaded using this form; instance will only update that specific record
        foodTagForm = TagForm(request.POST)

        print(form.data)
        print(foodImageForm.data)
        print(foodTagForm.data)
        
        # Food-datail form
        if form.is_valid():
            # Saving into DB
            # [ Further Development ]: Check if the restaurant-owner has the duplicate food record in the DB
            form.save()
            print('Hitting Food detail form-validation')
            # redirecting to the same food-detail page after updating food-information using the browser's url
            # https://stackoverflow.com/questions/57077059/how-do-i-redirect-to-the-same-page-after-an-action-in-django
            return HttpResponseRedirect(request.path_info)
        
        # Food-image form
        if foodImageForm.is_valid():
            print('Hitting Food image form-validation')
            foodImageForm.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        'title': 'Update Food Detail',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,
        'food_record': food_record,
        'form': form,
        'foodImageForm': foodImageForm,
        'foodTagForm': foodTagForm,
        'avgRating': avgRating,

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
    return render(request, 'food/update_detail_food_record.html', context)




# Delete a particular food item
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodRecordRemove(request, id):
    fRecord = Food.objects.get(pk=id)
    fRecord.delete()

    messages.info(request, 'A Food Record is removed: "%s"!' % fRecord.food_name)

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('foodApp:food_foodList')