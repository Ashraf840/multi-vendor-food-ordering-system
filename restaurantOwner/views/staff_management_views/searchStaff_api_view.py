from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from authentication.models import *


# This search can made by the restaurant-owner (optional: sys-admin)


# Used "axios.POST" to hit this view.
# Search Restaurant Staff
@csrf_exempt
def search_staff(request):
    if request.method == 'POST':
        # user = request.user  # Get the restaurant-user info

        # Fetch the input-text inserted by the restaurant-owner in the frontend.
        # searchFieldVal = request.POST.get('searchValue')
        # data = searchFieldVal

        # data = user
        # data = 'Hellow'

        data = json.loads(request.body)
        
        searchFieldVal = data.get('searchValue')
        restaurant_id = data.get('restaurant_id')

        # print('%s %s' % (('>'*10), searchFieldVal))
        print('%s %s' % (('>'*10), restaurant_id))


        # Make a query to the 'CustomUser' db-model for the restaurant staff that only belongs to that restaurant.
        # REQUIRED DATA: {
        #       'search-field' value typed by the user inside the search-box.
        #       'restaurant_id' of the logged-in restaurant-owner. [Done]
        # }

        # [ IMPORTANT ]
        # Refine the restaurant-name-input by removing all the non-alphaNumeric-Chars while a restaurant-owner is registering into the system.
        # Refinement is done in the "RestaurantOwnerRegistrationForm()" class inside the "foodsystem/authentication/forms.py" flie.


        # dict_data = {
        #     'searchFieldVal':searchFieldVal,
        #     'restaurant_id':restaurant_id,
        # }

        # For using 'and' inside the condition, use "&" inside the Q
        # For using 'or' inside the condition, use "&" inside the Q
        # [ B U G G E D ]: making blank <td> everytime making a query in the staff-list.
        staffs = CustomUser.objects.filter(
            ( Q(first_name__istartswith=searchFieldVal) |
            Q(last_name__istartswith=searchFieldVal) )
            &
            Q(restaurant_id__exact=restaurant_id)

            # rest-id is not matching, cause the " ' " (special character - apostrophy S) from the restaurant "Bachelor's" is conveting the 's as "&#x27;".
            # Thus always generalize the rest-name-field while registering in the system as restaurant-owner
            # restaurant_id=restaurant_id
        )

        data = staffs.values()

        # return JsonResponse(data, safe=False)
        # return JsonResponse(dict_data, safe=False)  # pass a dict as a jsonResponse
        return JsonResponse(list(data), safe=False)