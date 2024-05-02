from django.urls import path, include
from .views import (
    rc_index_views as rciv,
    rest_page_cust_view as rpcv,
    add_to_cart_views as atcv,
    cust_order_views as cov,
    cust_order_list_views as colv,
    restaurant_list_page_cust_views as rlpcv,
    loved_food_cust_view as lfcv,
)
from cartOrder.views import order_summary_views as osv
from cartOrder.views import payment_views as pymtv
# from cartOrder.views import 
# from .views import restaurant_staff_unapproved as rsu


app_name = 'restCustApp'


urlpatterns = [
    # [ Approved Staff Homepage ]
    path('', rciv.restaurant_customer_homepage, name='rcust_homepage'),

    # [ Unapproved Staff Homepage ]
    # path('unapproved/', rsu.rs_pending_index, name='rstaff_homepage_unapproved'),

    # [ Restaurant Page - Customer View ]
    path('restaurant-page/<int:id>/', rpcv.restaurant_page_cust_view, name='rest_page_cust_view'),

    # [ Add to cart - Restaurant Page - Customer View ]
    # path('resttaurant-page/add-to-cart/<str:cart>/<str:customer>/<str:food>', rpcv.addToCart, name='addToCart'),
    path('restaurant-page/add-to-cart/', rpcv.addToCart, name='addToCart'),

    # [ Food cart - Restaurant Page - Customer View ]
    path('restaurant-page/food-cart/<str:cartID>/', atcv.foodCart, name='foodCart'),

    # [ Food cart - Remove Cart Item - Restaurant Page - Customer View ]
    path('restaurant-page/food-cartItem-remove/<str:cartItemId>/', atcv.removeCartItem, name='foodCartItemRemove'),

    # [ Customer Food Order - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/<str:cartID>/', cov.customer_order, name='customerOrder'),

    # [ Customer Food Order - Delivery Detail Handle - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/delivery-detail/<str:cartID>/', cov.deliveryDetail, name='customerOrderDeliveryDetail'),

    # [ Customer Food Order - Personal Detail Handle - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/personal-detail/<str:customerID>/<str:cartID>/', cov.personalDetail, name='customerOrderPersonalDetail'),

    # [ Customer Food Order - Payment Method (COD) Handle - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/payment-method-COD/<str:orderID>/<str:cartID>/', cov.paymentMethodCOD, name='customerOrderPaymentMethodCOD'),

    # [ Customer Food Order - Payment Method (SSLCommerz) Handle - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/payment-method-SSLCommerz/<str:orderID>/<str:cartID>/', cov.paymentMethodSSLCommerz, name='customerOrderPaymentMethodSSLCommerz'),

    # [ Customer Food Order Payment Handle - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/payment/<str:orderID>/<str:cartID>/', pymtv.payment, name='customerOrderPayment'),

    # [ Customer Food Order Summary Handle - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/order-summary/<str:orderID>/<str:cartID>/', osv.orderSummary, name='customerOrderSummary'),

    # [ Customer Food Order Cancel - Restaurant Page (inherited) - Customer View ]
    path('restaurant-page/checkout/order-cancel/<str:orderID>/<str:cartID>/', osv.cancelOrder, name='customerOrderCancel'),


    # [ Customer Food Order List ]
    path('customer/food-order/list/', colv.customerOrderList, name='customerfoodOrderList'),

    # [ Customer Food Order Detail ]
    path('customer/food-order-detail/<str:orderID>/', colv.custOrderDetail, name='customerfoodOrderDetail'),

    # [ Customer Food Order Detail - Order Status - Cancel ]
    path('customer/food-order-detail/cancel/<str:orderID>/', colv.orderCancel, name='customerfoodOrderDetailCancel'),


    # [ Restaurant List - Customer View ]
    path('customer/restaurant-list/', rlpcv.restaurant_list_cust_view, name='restaurant_list_cust_view'),

    # [ Food Loved List - Customer View ]
    path('customer/loved-food-list/', lfcv.lovedFoodList, name='lovedFoodList'),

    # [ Food Loved - Remove - Customer View ]
    path('customer/loved-food-remove/<int:lovedFoodID>', lfcv.removeLovedFood, name='removeLovedFood'),
]
