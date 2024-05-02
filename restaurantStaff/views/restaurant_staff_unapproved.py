from django.shortcuts import render, redirect
from authentication.models import CustomUser
from userProfile.models import UserProfile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from authentication.decorators import *




# [ DECORATORS ]: stop restaurant staffs-approved, customers, unauthenticated users, anonymous users
@login_required(login_url='userAuth:login')
@stop_rest_staff
@stop_regular_cust
@stop_anonymous_user
def rs_pending_index(request):
    rest_staff = request.user
    # print(rest_staff.restaurant_id)

    rest_name_query = CustomUser.objects.get(
        Q(restaurant_id=rest_staff.restaurant_id)
        & Q(is_restaurant_owner='True')
    )

    # rest_staffs = CustomUser.objects.filter(
    #     Q(restaurant_id=rest_staff.restaurant_id)
    # )

    # # print(rest_name_query)
    # print(rest_staffs)


    # rso_dp = UserProfile.objects.filter(
    #     Q(user=rest_staff)
    # ).all()


    # print(rso_dp.profile_pic.url)
    # print(rso_dp)
    # for rdp in rso_dp:
    #     print(rso_dp.bio)

    # print(rest_name_query[0])
    # restaurant_name =  rest_name_query[0]
    # print(restaurant_name)

    context = {
        'title': 'Staff Pending HomePage',
        'rest_name_query': rest_name_query,
        # 'rest_staffs': rest_staffs,
    }
    return render (request, 'restaurantStaff/restaurant_staff_unapprvd.html', context)
