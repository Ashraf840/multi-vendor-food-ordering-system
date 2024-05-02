from django.db.models.signals import pre_save, post_save
# from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from userProfile.models import *


# NB:
# THIS FILE NEEDS TO BE IMPORTED in the apps.py file, 
# & install this project-app by using the exact same name "authentication.apps.AuthenticationConfig" 
# inside the INSTALLED_APPS of 'settings.py' to make it functional.



# Get the custom-user-model
User = get_user_model()



# newly created user will be automatically inactive, so they can't login without executing account activation through email
@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    if instance._state.adding is True:
        # Check if the user-creation-instance is neither of a superuser, admin or staff, then make the "is_active" disabled.
        # All the other users will be disabled while creating a DB record in the system.
        # print(type(instance))
        print('During adding instance via terminal - superuser status: %s' % instance.is_superuser)

        # By default, making all types of user's 'is_active' status to disabled
        instance.is_active = False
        # if instance.is_superuser != True or instance.is_admin != True or instance.is_staff != True:

        # Check if the user-creation-instance is other than a restaurant-staff, then the is_approved-field will be enabled
        if instance.is_restaurant_staff != True:
            instance.is_approved = True

        # # Check if superuser is getting created
        # if instance.is_superuser == False:
        #     print("Creating an Inactive User! Not superuser!")
        #     instance.is_active = False
        # else:
        #     instance.is_active = True
        #     print("Creating a superuser. Account activated!")
        #     # if instance.is_restaurant_staff != True:
        #     #     instance.is_approved = True
    # else:
    #     print("Updating User Record")
    
    print('After completing addition of instance via terminal - superuser status: %s' % instance.is_superuser)
    # If the user is a superuser, then automatically make the user account active.
    if instance.is_superuser == True:
        instance.is_active = True







# [ User Profile Creation ]
# **********************************************************************
# "User Profile Creation" youtube video link:  https://www.youtube.com/watch?v=jYzTKcvO0Pk
# **********************************************************************
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        print('User Profile is created using Signals!')



# [ Restaurant Profile Creation ]
# **********************************************************************
# "Restaurant Profile Creation" youtube video link:  https://www.youtube.com/watch?v=jYzTKcvO0Pk
# **********************************************************************
@receiver(post_save, sender=User)
def create_restaurant_profile(sender, instance, created, **kwargs):
    # [ Further Development ] Check if the created-instance is a restaurant-owner, using the ----->    kwargs['instance']
    # see "foodsystem\cartOrder\signals.py" file's "update_price" method for more details.
    if created:
        RestaurantProfile.objects.create(user=instance)
        
        print('Restaurant Profile is created using Signals!')
