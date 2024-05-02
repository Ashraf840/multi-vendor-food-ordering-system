from django.urls import path, include

from .views import (
    promo_code_views  as pcv
    , ro_index_views as roiv
)

from .views.food_order_views import (
    order_CRUD_views as ocv
    ,pending_order_views as pov
)

from .views.staff_management_views import (
    staff_recruit_remove_views as strrv
    ,searchStaff_api_view as srchsav
)

# from .views.food_statistics_views import customer_wishlist as cwl
from .views.food_statistics_views import customer_wishlist as cwl

from django.views.decorators.csrf import csrf_exempt



app_name = 'restOwnerApp'


urlpatterns = [
    path('', roiv.restaurant_owner_homepage, name='rowner_homepage'),  # homepage for both the restaurant owner & staff

    # Staff Recuitement Endpoints
    path('staff_list/', strrv.staff_list, name='rowner_staff_list'),
    path('staff_list_pending/', strrv.staff_list_pending, name='rowner_pending_staff_list'),
    path('staff_approval/<int:id>/', strrv.staff_approval, name='rowner_staff_approval'),
    path('staff_remove/<int:id>/', strrv.delete_staff, name='rowner_staff_delete'),
    path('staff_suspend/<int:id>/', strrv.restStaff_suspend, name='rowner_staff_suspend'),
    path('staff_unsuspend/<int:id>/', strrv.restStaff_unsuspend, name='rowner_staff_unsuspend'),

    # [ Food Promo Codes + Create Promo Code ]
    path('food/promo-code/', pcv.promoCodeList, name='rowner_promo_code_list'),

    # [ Food Addon Update: Make addon "Not Avaiable" ]
    path('food/promo-code/make-not-available/<int:id>/', pcv.promoCodeStatUpdate_makeUnavailable, name='promoCodeStatUpdate_makeUnavailable'),

    # [ Food Addon Update: Make addon "Avaiable" ]
    path('food/promo-code/make-available/<int:id>/', pcv.promoCodeStatUpdate_makeAvailable, name='promoCodeStatUpdate_makeAvailable'),

    # [ Food Promo Codes Remove ]
    path('food/promo-code-remove/<int:id>', pcv.promoCodeRemove, name='rowner_promo_code_delete'),

    
    # Staff Search Endpoint, which is using the view "search_staff" inside the "restaurantOwner/views/staff_management_views/staff_recruit_remove_views.py" file.
    path('staff_search/', csrf_exempt(srchsav.search_staff), name='rowner_staff_search'),

    # [ Food Orders List ]
    path('food_order/list/', ocv.orderList, name='food_order_list'),

    # [ Food Orders List ]
    path('food_order/staus-update/<str:order_id>', ocv.restaurant_order_status_update, name='restaurant_order_status_update'),

    # [ Food Orders Paid/Unpaid ]
    path('food_order/staus-update/paid-unpaid/<str:order_id>', ocv.restaurant_order_paidUnpaid_update, name='restaurant_order_paidUnpaid_update'),



    # [ Food Orders Pending - Foods that doesn't updated to the "order received by the customer" status ]
    path('food_order/pending-food-orders/', pov.pendingOrderList, name='restaurant_pendingOrderList'),


    # [ Customer Food Wishlist - Foods that are loved ny the customer ]
    path('statistics/customer-wishlist/', cwl.restaurant_customer_wishlist, name='restaurant_customer_wishlist'),
]
