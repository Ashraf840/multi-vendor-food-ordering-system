from django.shortcuts import render, redirect
from authentication.models import CustomUser
from django.db.models import Q  # to make complex queries
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.helper_functions.export_user_profile import export_user_profile
from food.models import Tag
from food.forms import TagForm
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from authentication.decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages




# Food Tag List Method + Add New Tag Method
# [ DECORATORS: Only restaurant-owner can create food-tags ]: first set the decorators on this view then hide the food-tags-option from the side-nav-panel.
# Tag shouldn't be viewed or edited by the restaurant-staffs for security-issues. Also it'will be used in the ML Model.
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodTagList(request):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Render the empty form of "Food-Tag"; along with the food-tag-list
    form = TagForm()

    # Get the user-type, which will be displayed as the center-top panel of the page.
    user_type = get_user_type(userInfo)

    # Get the specific class-object of the restaurant-owner (Specific user-data)
    user_detail = CustomUser.objects.get(
        Q(email=userInfo.email)
    )

    # Fetch the Restaurant ID, so that it can be passed to the "base_restaurant_owner.html" -> the inline-js -> searchStaff_api.js
    rest_id = user_detail.restaurant_id
    print("%s Restaurant ID: %s %s" % ( ('*'*10), (rest_id), ('*'*10) ))


    # [ HELPER FUNCTION ]: to grab the user-profile-data.
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    u_profile = export_user_profile(userID = u_id)


    # Make a query to fetch the food-tag-names of the specific restaurant-owner-staff
    food_tags = Tag.objects.filter(
        Q(created_by=u_id)
    ).all()

    print(food_tags)


    # Make the POST-request for the TagForm. (Add new tag)
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():

            # [ Futher Developement ]:  Set the tag insertion procedure in a helper-function
            tagName = form.cleaned_data['tag_name']     # fetched from "name" attr from the frontend, but the frontend "name" attr is getting the name-value fron the model-field ("tag_name") of the "Tag" DB-model.
            
            # Add a hash-tag at the beginning of each tag-name before inserting in the DB
            tagName = '#' + tagName
            print(tagName)

            # Check if the food-tag is already exist in the DB
            tagName_db_query = Tag.objects.filter(tag_name=tagName)

            signl = '>' * 10
            signr = '<' * 10

            # Check tag-name duplicacy
            if tagName_db_query:
                print('%s Found Duplicate %s' % (signl, signr))
                messages.info(request, 'Tag already exists!')
            else:
                print('%s Allowed to insert a new food-tag-name %s' % (signl, signr))
                # print(request.user.id)
                Tag.objects.create(tag_name=tagName, created_by=request.user)
                messages.info(request, 'New Tag Created: "%s"!' % tagName)
                return HttpResponseRedirect(reverse('foodApp:food_foodTagList'))


    context={
        'title': 'Food Tag List',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,
        'food_tags': food_tags,
        'form': form,
    }
    return render(request, 'food/food_tag_list.html', context)






# Food Tag Remove Method
# [ DECORATORS: Only restaurant-owner can delete food-tags ]
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodTagRemove(request, id):
    fTag = Tag.objects.get(pk=id)
    fTag.delete()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('foodApp:food_foodTagList')


