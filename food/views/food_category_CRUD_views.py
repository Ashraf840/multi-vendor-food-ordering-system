from django.shortcuts import render, redirect
from food.forms import CategoryForm
from userProfile.helper_functions.export_user_profile import export_user_profile
from authentication.helper_functions.identify_user_type import get_user_type
from django.db.models import Q  # to make complex queries
from food.models import Category
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from authentication.decorators import *





@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
# Food Category List + Create Food Category
def foodCategoryList(request):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Render the empty form of "Food-Category"; along with the food-category-list
    form = CategoryForm()

    # Get the user-type, which will be displayed as the center-top panel of the page.
    user_type = get_user_type(userInfo)


    # [ HELPER FUNCTION ]: to grab the user-profile-data.
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    u_profile = export_user_profile(userID = u_id)

    # Make a query to fetch the food-category-names of the specific restaurant-owner-staff
    # food_category = Category.objects.filter(
    #     Q(created_by=u_id)
    # ).all()

    food_category = Category.objects.all()

    print(food_category)


    # Make the POST-request for the CategoryForm. (Add new Category)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            categoryName = form.cleaned_data['cate_name']     # fetched from "name" attr from the frontend, but the frontend "name" attr of the form-field is getting the name-value fron the form-field ("category_name") of the "Category" DB-model.

            # Make a query to the DB whether the category already exists.
            food_category_db_query = Category.objects.filter(
                Q(cate_name=categoryName)
            ).all()
            
            print(food_category_db_query)

            signl = '>' * 10
            signr = '<' * 10

            # Check if the category-name already exists in the DB
            if food_category_db_query:
                print('%s Found Duplicate %s' % (signl, signr))
                messages.info(request, 'Food-category already exists!')
            else:
                print('%s Allowed to insert a new Food-category-name %s' % (signl, signr))
                
                # # Create new food-category
                Category.objects.create(cate_name=categoryName)
                messages.info(request, 'New Category Created: "%s"!' % categoryName)
                return HttpResponseRedirect(reverse('foodApp:food_foodCategoryList'))

    context = {
        'title': 'Food Category List',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,
        'food_category': food_category,
        'form': form,
    }
    return render(request, 'food/food_category_list.html' ,context)




@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodCategoryRemove(request, id):
    fCategory = Category.objects.get(pk=id)
    fCategory.delete()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('foodApp:food_foodCategoryList')
