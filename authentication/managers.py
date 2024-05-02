# Create your models here.
from django.contrib.auth.models import BaseUserManager



# # Manager class to manage user-model (Super & Regular User)
# class CustomUserManager(BaseUserManager):
#     # Create regular users
#     def create_user(self, email, company_name, first_name, last_name, gender, phone, password=None):
#         # Check basic validations for the required fields of "CustomUser" class
#         if not email:
#             raise ValueError('Email is required!')
        
#         #  Create a user model
#         user = self.model(
#             email=self.normalize_email(email),
#             company_name=company_name,
#             first_name=first_name,
#             last_name=last_name,
#             gender=gender,
#             phone=phone
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


#     # Create superusers
#     def create_superuser(self, email, company_name, first_name, last_name, gender, phone, password=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             company_name=company_name,
#             first_name=first_name,
#             last_name=last_name,
#             gender=gender,
#             phone=phone,
#             password=password
#         )
#         user.set_password(password)
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user








# Manager class to manage user-model (Super & Regular User)
class CustomUserManager(BaseUserManager):
    # Create regular users
    def create_user(self, email, company_name, first_name, last_name, gender, phone, password=None):
        # Check basic validations for the required fields of "CustomUser" class
        if not email:
            raise ValueError('Email is required!')
        
        #  Create a user model
        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    # Create superusers
    def create_superuser(self, email, company_name, first_name, last_name, gender, phone, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            company_name=company_name,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone=phone,
            password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user






