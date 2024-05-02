from django.urls import path, include
from . import views
from . import emailVerification as ev

from . import auth_testing_views as atv

app_name = 'authApp'

urlpatterns = [
    path('user_login/', views.userLogin, name='login'),
    # Regular Customer Signup
    path('user_signup/', views.userReg, name='registration'),
    # Restaurant Owner Signup
    path('user_restaurant_owner_signup/', views.restaurantOwnerReg, name='registrationRestOwner'),
    # Restaurant Staff Signup
    path('user_restaurant_staff_signup/', views.restaurantStaffReg, name='registrationRestStaff'),
    # User Logout
    path('user_logout/', views.userLogout, name='logout'),

    # Email Verification Endpoints
    # User Account Activation [ Tokenized activation url ]
    path('activate/<uidb64>/<token>/', ev.VerificationView.as_view(), name='activate'),      # the name 'activate' is used in the 'link' variable of 'activate_url'


    # Testing Auth Decorators (Endpoints)
    path('test_sys_admin/', atv.check_sysAdmin, name='sysAdmin_homepage'),
    path('test_res_owner/', atv.check_res_owner, name='res_owner_homepage'),
    path('test_res_staff/', atv.check_res_staff, name='res_staff_homepage'),
    path('test_res_staff_unapproved/', atv.check_res_staff_unapproved, name='res_staff_unapproved_homepage'),
    path('test_regular_cust/', atv.check_regularCust, name='regular_cust_homepage'),
    path('test_anonymous_cust/', atv.check_anonymousCust, name='anonymous_cust_homepage'),

    # Common Redirect Page
    path('test_common_redirect_page_before_login/', atv.common_redirect_page_before_login, name='common_redirect_page_before_login'),
    path('test_common_redirect_page_after_login/', atv.common_redirect_page_after_login, name='common_redirect_page_after_login'),

    # [ FURTHER DEVELOPMENT ]
    # Create homepage views for each user role (rest_owner, rest_staff, regular_cust, anonymous_cust) in their own app's "view-funcs",
    # then call them in this urls.py, cause the decoretors are built here,
    # then USE THESE ENDPOINTS IN THE DECORATORS FOR REDIRECTION.
]