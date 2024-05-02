from django.urls import path, include
# from .views import rs_index_views as rsiv 
# from .views import restaurant_staff_unapproved as rsu
from .views import (
    rs_index_views as rsiv
    ,restaurant_staff_unapproved as rsu
    ,order_list_staff_view as olsv
)


app_name = 'restStaffApp'


urlpatterns = [
    # [ Approved Staff Homepage ]
    path('', rsiv.restaurant_staff_homepage, name='rstaff_homepage'),

    # [ Unapproved Staff Homepage ]
    path('unapproved/', rsu.rs_pending_index, name='rstaff_homepage_unapproved'),


    # [ Restaurant Order List - Staff View ]
    path('restaurant-order-list/staff-view/', olsv.orderList_staff_view, name='orderList_staff_view'),
]
