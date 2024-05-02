from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager   # Manages "Super & Regular Users"
import string, random


"""
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Manager class to manage user-model (Super & Regular User) is in the "authentication/managers.py" file.
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""


# >>>>>>>>>>>>>>>>>>>>>> MUltiple User Creation Model <<<<<<<<<<<<<<<<<<<<<<



# Custom User Model
# 'AbstractBaseUser' provides the core functionalities of the user-authentication system. 
# Like the password-hashing, session-storing and recognizing sessions on the tokenizing, password-reset etc.
# These functionalities are inherited from the 'AbstractBaseUser' class.
CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


# Restaurant Owner Account Creation - Model
# This method will generate a random-string of 8 chars.
def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



# Regular User (Consumers)
class CustomUser(AbstractBaseUser):
    # User Info
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    company_name = models.CharField(verbose_name='Company Name', max_length=200, blank=True, default='Not Available')
    phone = models.CharField(verbose_name='Company Phone', max_length=20, blank=True, default='Null')
    # User Info [Extra]
    first_name = models.CharField(verbose_name='First Name', max_length=50, blank=True, default='Anonymous')
    last_name = models.CharField(verbose_name='Last Name', max_length=50, blank=True, default='User')
    gender = models.CharField(verbose_name='Gender', max_length=10, choices=CHOICES, default='Male')

    # Restaurant Owner + Staff Info
    restaurant_name = models.CharField(max_length=100, blank=True, unique=True, null=True)
    restaurant_id = models.CharField(max_length=150, blank=True, null=True)
    tin_number = models.CharField(max_length=50, blank=True, unique=True, null=True)
    # profile_pic = models.ImageField(upload_to='profilePicture', default='profilePicture/default_dp.png', blank=True, null=True)
    # profile_pic = models.ImageField(upload_to='profilePicture', blank=True, null=True)

    rest_profile_pic = models.ImageField(upload_to='profilePicture', blank=True, null=True)


    # Registration
    date_joined = models.DateField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)

    # Extend Roles & Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_restaurant_owner = models.BooleanField(default=False)
    is_restaurant_staff = models.BooleanField(default=False)
    is_regular_user = models.BooleanField(default=False)
    is_anonymous_user = models.BooleanField(default=False)
    # Restaurant Staff Approval Permission
    is_approved = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "User"

    # Main field for authentication
    # Email address will be the primary user-identifier instead of a username for authentication.
    USERNAME_FIELD = 'email'

    # When creating admin-user-accounts, the following fields are required to be filled, bcz it'll call the "create_superuser()"  method from the "CustomUserManager()" class.
    # (generally the initial admin is created using the terminal)
    REQUIRED_FIELDS = ['company_name', 'phone', 'first_name', 'last_name', 'gender']

    # Define the base user model manager
    objects = CustomUserManager()

    # User Detail page from the administration panel
    def __str__(self) -> str:
        if self.is_restaurant_owner == True:
            # return 'Restaurant: ' + self.restaurant_name
            return self.restaurant_name
        elif self.is_restaurant_staff == True:
            # return 'Restaurant Staff: ' + self.first_name + ' ' + self.last_name
            return self.first_name + ' ' + self.last_name
        elif self.is_regular_user == True:
            # return 'Regular User: ' + self.first_name + ' ' + self.last_name
            # return self.first_name + ' ' + self.last_name
            return self.first_name
        elif self.is_anonymous_user == True:
            # return 'Anonymous User: ' + self.first_name + ' ' + self.last_name
            return self.first_name + ' ' + self.last_name
        else:
            return self.company_name

    def get_full_name(self):
        """
        While this models gets queried, it returns the fullnames consisting of first+last name
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        # "Returns the short name for the user."
        return self.first_name

    # The signing-up user is going to have any permission (defined later), it'll just return true. 
    # If it returns false, the authorization will immediately fail & django won't check the backend that follow.
    def has_perm(self, perm, obj=None):
        return True
    
    # The scope to assign signup users whether to have permissions to access to other models in this django-project.
    def has_module_perms(self, app_label):
        return True


    # Get the profile picture of a user.
    # [ PROBLEM SOLVED ]: https://newbedev.com/django-the-image-attribute-has-no-file-associated-with-it
    @property
    def get_rest_photo_url(self):
        if self.rest_profile_pic and hasattr(self.rest_profile_pic, 'url'):
            return self.rest_profile_pic.url
        else:
            return "/media/rProfilePicture/default_rest_dp.jpg"
    

    
    def save(self, *args, **kwargs):
        try:
            # [ SECURITY CHECK ]
            # [ Reasong for making this custom-condition ] Only generate restaurant id only while creating an account for the first time. 
            # Prohibit updating the restaurant_id while updating any other field of that specific rest_owner_account.
            if self.restaurant_name is not None and self.restaurant_id is None:
                # res_name_tuned = self.restaurant_name.replace(" ", "_")
                # Remove all the non-alphanumeric chars from the restaurant-name while generating the rest-id.
                res_name_tuned = ''.join(s for s in self.restaurant_name if s.isalnum())
                # print('%s Restaunrant Name(ModelForm) - After tuned: %s %s' % (sign, res_name_tuned, sign))
                # user.restaurant_name = res_name_tuned
                self.restaurant_id = res_name_tuned + "_" + self.tin_number + "_" + random_string_generator()
            
            # Check if the user is a restaurant-owner, it True, then add a default restaurant profile pic.
            if self.is_restaurant_owner:
                self.rest_profile_pic = 'rProfilePicture/default_rest_dp.jpg'
                # pass
        except:
            return True
        super(CustomUser, self).save(*args, **kwargs)






# # Regualr User Model
# class RegularUser(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
#     email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
#     phone = models.CharField(verbose_name='Company Phone', max_length=20, blank=True, default='Null')
#     pass













# # Restaurant Owner Account Creation - Model
# # This method will generate a random-string of 8 chars.
# def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))



# # Restaurant Owner (as a User)
# class RestaurantOwner(models.Model):
#     # Restaurant Info
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     # solution_company_name = models.CharField(verbose_name='Company Name', max_length=200, blank=True, default='Not Available')
#     restaurant_name = models.CharField(max_length=100, blank=False, unique=True)
#     restaurant_id = models.CharField(max_length=30, blank=False, unique=True)
#     tin_number = models.CharField(max_length=50, blank=False, unique=True)
#     email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
#     # User Info [Extra]
#     first_name = models.CharField(verbose_name='First Name', max_length=50, blank=True, default='Anonymous')
#     last_name = models.CharField(verbose_name='Last Name', max_length=50, blank=True, default='User')
#     gender = models.CharField(verbose_name='Gender', max_length=10, choices=CHOICES, default='Male')
#     # Registration
#     date_joined = models.DateField(verbose_name='Date Joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)
#     phone = models.CharField(verbose_name='Company Phone', max_length=20, blank=True, default='Null')
#     # Permissions
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     # Extend Roles
#     is_restaurant_owner = models.BooleanField(default=True)
#     is_restaurant_staff = models.BooleanField(default=False)
#     is_regular_user = models.BooleanField(default=False)
#     is_anonymous_user = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = "User - Resraurant Owner"

#     REQUIRED_FIELDS = ['user', 'restaurant_name', 'tin_number']

#     # def __str__(self) -> str:
#     #     # return self.restaurant_name
#     #     return self.user

#     # overriding 'save' method to generate random-string while creating an restaurant_owner-account using the "random_string_generator" method
#     def save(self, *args, **kwargs):
#         # If no 'order_id' isn't passed while creating an order.
#         # if not len(self.order_id):
#         #     self.order_id = random_string_generator()
#         res_name_tuned = self.restaurant_name.replace(" ", "_")
#         self.restaurant_id = res_name_tuned + "_" + self.tin_number + "_" + random_string_generator()
#         super(RestaurantOwner, self).save(*args, **kwargs)







# # Restaurant Owner (as a User)
# class RestaurantOwner(AbstractBaseUser):
#     # Restaurant Owner Info [Extra]
#     email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
#     first_name = models.CharField(verbose_name='First Name', max_length=50, blank=True, default='Anonymous')
#     last_name = models.CharField(verbose_name='Last Name', max_length=50, blank=True, default='User')
#     gender = models.CharField(verbose_name='Gender', max_length=10, choices=CHOICES, default='Male')
#     # Restaurant Info [Extra]
#     restaurant_name = models.CharField(max_length=100, blank=False, unique=True)
#     phone = models.CharField(verbose_name='Company Phone', max_length=20, blank=True, default='Null')
#     restaurant_id = models.CharField(max_length=30, blank=False, unique=True)
#     tin_number = models.CharField(max_length=50, blank=False, unique=True)
#     # Registration
#     date_joined = models.DateField(verbose_name='Date Joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)
#     # Permissions
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     # Extend Roles
#     is_restaurant_owner = models.BooleanField(default=True)
#     is_restaurant_staff = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = "Resraurant Owner List"

#     # Main field for authentication
#     # Email address will be the primary user-identifier instead of a username for authentication.
#     USERNAME_FIELD = 'email'

#     # When creating admin-user-accounts, the following fields are required to be filled, bcz it'll call the "create_superuser()"  method from the "CustomUserManager()" class.
#     # (generally the initial admin is created using the terminal)
#     REQUIRED_FIELDS = ['restaurant_name', 'tin_number', 'phone', 'first_name', 'last_name']

#     # Define the base user model manager
#     objects = CustomUserManager()

#     def __str__(self) -> str:
#         return self.restaurant_name

#     # overriding 'save' method to generate random-string while creating an restaurant_owner-account using the "random_string_generator" method
#     def save(self, *args, **kwargs):
#         # If no 'order_id' isn't passed while creating an order.
#         # if not len(self.order_id):
#         #     self.order_id = random_string_generator()
#         res_name_tuned = self.restaurant_name.replace(" ", "_")
#         self.restaurant_id = res_name_tuned + "_" + self.tin_number + "_" + random_string_generator()
#         super(RestaurantOwner, self).save(*args, **kwargs)


#     def get_full_name(self):
#         """
#         Returns the first_name plus the last_name, with a space in between.
#         """
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
    
#     def get_short_name(self):
#         # "Returns the short name for the user."
#         return self.first_name

#     # The signing-up user is going to have any permission (defined later), it'll just return true. 
#     # If it returns false, the authorization will immediately fail & django won't check the backend that follow.
#     def has_perm(self, perm, obj=None):
#         return True
    
#     # The scope to assign signup users whether to have permissions to access to other models in this django-project.
#     def has_module_perms(self, app_label):
#         return True





# # Set a condition to check if the restaurant_id entered by the restaurant_staff is matched/ exists in that specific restaurant row.



# # Restaurant Staff (as a User)
# class RestaurantStaff(AbstractBaseUser):
#     # Restaurant Staff Info
#     email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
#     phone = models.CharField(verbose_name='Phone', max_length=20, blank=True, default='Null')
#     first_name = models.CharField(verbose_name='First Name', max_length=50, blank=True, default='Anonymous')
#     last_name = models.CharField(verbose_name='Last Name', max_length=50, blank=True, default='User')
#     gender = models.CharField(verbose_name='Gender', max_length=10, choices=CHOICES, default='Male')

#     # Restaurant Info [Extra]
#     restaurant = models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE)
#     # restaurant_id = models.CharField(max_length=30, blank=False, unique=True)
#     # tin_number = models.CharField(max_length=50, blank=False)
#     # Registration

#     date_joined = models.DateField(verbose_name='Date Joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)
#     # Permissions
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     # Extend Roles
#     is_restaurant_owner = models.BooleanField(default=False)
#     is_restaurant_staff = models.BooleanField(default=True)

#     class Meta:
#         verbose_name_plural = "Resraurant Staff List"

#     # Main field for authentication
#     # Email address will be the primary user-identifier instead of a username for authentication.
#     USERNAME_FIELD = 'email'

#     # When creating admin-user-accounts, the following fields are required to be filled, bcz it'll call the "create_superuser()"  method from the "CustomUserManager()" class.
#     # (generally the initial admin is created using the terminal)
#     REQUIRED_FIELDS = ['restaurant', 'phone', 'first_name', 'last_name', 'gender']

#     # Define the base user model manager
#     objects = CustomUserManager()

#     def __str__(self) -> str:
#         return (self.first_name + ' ' + self.last_name)

#     # # overriding 'save' method to generate random-string while creating an restaurant_owner-account using the "random_string_generator" method
#     # def save(self, *args, **kwargs):
#     #     # If no 'order_id' isn't passed while creating an order.
#     #     # if not len(self.order_id):
#     #     #     self.order_id = random_string_generator()
#     #     res_name_tuned = self.restaurant_name.replace(" ", "_")
#     #     self.restaurant_id = res_name_tuned + "_" + self.tin_number + "_" + random_string_generator()
#     #     super(RestaurantOwner, self).save(*args, **kwargs)


#     def get_full_name(self):
#         """
#         Returns the first_name plus the last_name, with a space in between.
#         """
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
    
#     def get_short_name(self):
#         # "Returns the short name for the user."
#         return self.first_name

#     # The signing-up user is going to have any permission (defined later), it'll just return true. 
#     # If it returns false, the authorization will immediately fail & django won't check the backend that follow.
#     def has_perm(self, perm, obj=None):
#         return True
    
#     # The scope to assign signup users whether to have permissions to access to other models in this django-project.
#     def has_module_perms(self, app_label):
#         return True

