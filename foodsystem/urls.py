"""foodsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Library for Media URL Config
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include(('authentication.urls', 'app_name'), namespace='userAuth')),
    
    path('home/', include(('home.urls', 'app_name'), namespace='homeApplication')),
    
    path('restaurant-owner/', include(('restaurantOwner.urls', 'app_name'), namespace='restaurantOwnerApplication')),
    path('restaurant-staff/', include(('restaurantStaff.urls', 'app_name'), namespace='restaurantStaffApplication')),
    path('restaurant-customer/', include(('restaurantCustomer.urls', 'app_name'), namespace='restaurantCustomerApplication')),

    path('food/', include(('food.urls', 'app_name'), namespace='foodApplication')),
    path('cart-order/', include(('cartOrder.urls', 'app_name'), namespace='cartOrderApplication')),
]




# Media File URL Configuration (in the development stage)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

