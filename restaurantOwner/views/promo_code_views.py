from django.shortcuts import render, redirect
from authentication.helper_functions.identify_user_type import get_user_type
from userProfile.models import UserProfile
from restaurantOwner.models import PromoCode
from django.db.models import Q
from restaurantOwner.forms import PromoCodeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from authentication.decorators import *





# [ DECORATORS ]
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
@stop_rest_staff_unapproved
def promoCodeList(request):
    # Get the user-information of that particular user.
    userInfo = request.user

    # Get the user_type identification func from the "foodsystem/authentication/helper_functions/identify_user_type.py" files.
    user_type = get_user_type(userInfo) # Get the user-type; whether the user is a staff/ customer

    # Render the empty form of "Food-Category"; along with the food-category-list
    form = PromoCodeForm()

    # print(request.user.id)
    # Get user profile of this specific restaurant-staff
    u_id = request.user.id

    u_profile = UserProfile.objects.get(id=u_id)

    promo_code = PromoCode.objects.filter(
        Q(rest_owner=u_id)
    ).all()

    print(promo_code)

    # Create new promo code
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            promoCodeName = form.cleaned_data['promo_code_name']
            rest_owner = userInfo
            discountPrice = form.cleaned_data['discount_price']

            PromoCode.objects.create(
                promo_code_name=promoCodeName,
                rest_owner=rest_owner,
                discount_price=discountPrice
            )

            messages.info(request, 'New Promo Code Created: "%s"!' % promoCodeName)
            return HttpResponseRedirect(reverse('restOwnerApp:rowner_promo_code_list'))


    context = {
        'title': 'Promo Code',
        'user_type': user_type,
        'u_profile': u_profile,
        'promo_code': promo_code,
        'form': form,
    }
    return render(request, 'restaurantOwner/promo_code_list.html', context)




# [ Decorators ]
# Views without using a dj-form to interact with the DB (more like the "remove" method)
def promoCodeStatUpdate_makeUnavailable(request, id):
    promoCode = PromoCode.objects.get(pk=id)
    promoCode.is_available = False
    promoCode.save()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('restOwnerApp:rowner_promo_code_list')




# [ Decorators ]
# Views without using a dj-form to interact with the DB (more like the "remove" method)
def promoCodeStatUpdate_makeAvailable(request, id):
    promoCode = PromoCode.objects.get(pk=id)
    promoCode.is_available = True
    promoCode.save()

    # [ FURTHER DEVELOPMENT ]: Redirect to the same page, using dynamic func
    return redirect('restOwnerApp:rowner_promo_code_list')








# [ Decorators ]
def promoCodeRemove(request, id):
    promoCode = PromoCode.objects.get(pk=id)
    promoCode.delete()

    return redirect('restOwnerApp:rowner_promo_code_list')


