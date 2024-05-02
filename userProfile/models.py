from django.db import models
from authentication.models import CustomUser
from django.utils import timezone



# --------------------------------------
# This application is used for user-Profiles as well as restaurant profiles.
# --------------------------------------


# General User Profile
class UserProfile(models.Model):
    # user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profilePicture', blank=True, null=True)

    class Meta():
        verbose_name_plural = 'User Profile'

    def __str__(self):
        return str(self.user)
    
    # Get the profile picture of a user.
    # [ PROBLEM SOLVED ]: https://newbedev.com/django-the-image-attribute-has-no-file-associated-with-it
    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/media/profilePicture/default_dp.png"






# Restaurant PRofile db-model
class RestaurantProfile(models.Model):
    # user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)

    # "TimeField" ref link:  https://www.geeksforgeeks.org/timefield-django-models/
    # opening_time = models.TimeField(auto_now=False, auto_now_add=True, blank=True, null=True, editable=True)
    # closing_time = models.TimeField(auto_now=False, auto_now_add=True, blank=True, null=True, editable=True)

    opening_time = models.TimeField(blank=True, null=True, default=timezone.now)
    closing_time = models.TimeField(blank=True, null=True, default=timezone.now)

    is_closed = models.BooleanField(default=False)

    restaurant_profile_pic = models.ImageField(upload_to='rProfilePicture', default='rProfilePicture/default_rest_dp.jpg', blank=True, null=True)

    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    class Meta():
        verbose_name_plural = 'Restaurant Profile'

    def __str__(self):
        return str(self.user)
    
    # Get the profile picture of a user.
    # [ PROBLEM SOLVED ]: https://newbedev.com/django-the-image-attribute-has-no-file-associated-with-it
    @property
    def get_rest_photo_url(self):
        if self.restaurant_profile_pic and hasattr(self.restaurant_profile_pic, 'url'):
            return self.restaurant_profile_pic.url
        else:
            return "/media/rProfilePicture/default_rest_dp.jpg"