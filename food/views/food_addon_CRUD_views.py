from django.shortcuts import render, redirect
from food.forms import AddonForm
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.helper_functions.export_user_profile import export_user_profile
from food.models import Addon
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from authentication.decorators import *





# Food Addon List
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodAddonList(request):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Render the empty form of "Food-Addon"; along with the food-addon-list
    form = AddonForm()

    # Get the user-type, which will be displayed as the center-top panel of the page.
    user_type = get_user_type(userInfo)

    # [ HELPER FUNCTION ]: to grab the user-profile-data.
    # Get the user-profile model (intially get the user-profile-picture)
    # Made a helper-function to grab the user-profile of a particualr-user. Inside the "userProfile\helper_functions\export_user_profile.py" file.
    u_id = request.user.id
    u_profile = export_user_profile(userID = u_id)

    # Make a query to fetch the food-tag-names of the specific restaurant-owner-staff
    food_addons = Addon.objects.filter(
        Q(created_by=u_id)
    ).all()

    print(food_addons)


    # Make a post request to create new food-addon
    # Firstly, check if the specific restaurant-owner has the same addon previously.
    if request.method == 'POST':
        form = AddonForm(request.POST)
        if form.is_valid():
            # print('Addon is going to be added!')
            addonName = form.cleaned_data['addon_name']
            addonPrice = form.cleaned_data['price']
            # print('Addon Name: %s' % addonName)
            # print('Addon Price: %s' % addonPrice)
            # print('Restaurant Owner: %s' % userInfo)

            # Check if the food-addon of the specific restaurant-owner exists in the DB
            AddonName_db_query = Addon.objects.filter(addon_name=addonName, created_by=userInfo)

            signl = '>' * 10
            signr = '<' * 10

            if AddonName_db_query:
                print('%s Duplicate addon found! %s' % (signl, signr))
                messages.info(request, 'Addon already exists!')
            else:
                print('%s Allow to create new addon! %s' % (signl, signr))
                Addon.objects.create(addon_name=addonName, created_by=userInfo, price=addonPrice)
                messages.info(request, 'New Addon Created: "%s"!' % addonName)
                return HttpResponseRedirect(reverse('foodApp:food_foodAddonList'))



    context = {
        'title': 'Food Addon List',
        'user_type': user_type,
        'u_profile': u_profile,
        'userInfo': userInfo,
        'food_addons': food_addons,
        'form': form,
    }
    return render(request, 'food/food_addon_list.html', context)




# Make food addons unavailable
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
# Views without using a dj-form to interact with the DB (more like the "remove" method)
def foodAddonStatUpdate_makeUnavailable(request, id):
    fAddon = Addon.objects.get(pk=id)
    fAddon.is_available = False
    fAddon.save()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('foodApp:food_foodAddonList')





# Make food addons available
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
# Views without using a dj-form to interact with the DB (more like the "remove" method)
def foodAddonStatUpdate_makeAvailable(request, id):
    fAddon = Addon.objects.get(pk=id)
    fAddon.is_available = True
    fAddon.save()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('foodApp:food_foodAddonList')





# Remove food addons
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def foodAddonRemove(request, id):
    fAddon = Addon.objects.get(pk=id)
    fAddon.delete()

    return redirect('foodApp:food_foodAddonList')

