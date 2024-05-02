from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import *
from django.contrib.auth import authenticate
from django.db import transaction  # What is transaction????? <<<<<<<<<<<<<<<<<<<<<<<<<<




CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


# >>>>>>>>>>>>>>>>>>>>>>> Use Signals.py to make any user-type registration an default inactive account


# Regular User Registration Form
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone', 'password1', 'password2']
        widgets = {
            'email' : forms.EmailInput(attrs = {'placeholder': 'Email', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    
    # Override the save method of the restaurant-staff account creation.
    # Define the user-row as the restaurant-owner in the model
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_regular_user = True
        user.is_approved = True
        user.save()
        return user





# Restaurant Owner Account Creation
class RestaurantOwnerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    restaurant_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Restaurant Name', 'class': 'form-control'}))
    tin_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'TIN Number', 'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=CHOICES)

    class Meta(UserCreationForm.Meta):
        # model = RestaurantOwner
        model = CustomUser

        fields = ['email', 'first_name', 'last_name', 'gender', 'phone', 'restaurant_name', 'tin_number', 'password1', 'password2']
        widgets = {
            'email' : forms.EmailInput(attrs = {'placeholder': 'Email', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RestaurantOwnerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    

    # Override the save method of the restaurant-staff account creation.
    # Define the user-row as the restaurant-owner in the model
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_restaurant_owner = True
        user.is_approved = True

        
        # ------------------------------------------------------------------------------------------
        # [ SECURITY CHECK ]
        # If there is any non-alphaNumeric characters inside the restaurant-name,
        # then remove all the non-alphaNumeric characters from the restaurant-name. 
        # [ Reason ] Because, it's making an issue while making query in the 'search_staff' method 
        # inside the "foodsystem/restaurantOwner/views/staff_management_views/searchStaff_api_view.py" file.


        # [testing]
        # sign = 'X'*20
        # print('%s Restaunrant Name(ModelForm): %s %s' % (sign, user.restaurant_name, sign))

        # remove all non-alphaNumeric chars using the join() method by using nothing, cause join() works with iterable.
        # res_name_tuned = ''.join(s for s in user.restaurant_name if s.isalnum())
        # # print('%s Restaunrant Name(ModelForm) - After tuned: %s %s' % (sign, res_name_tuned, sign))
        # user.restaurant_name = res_name_tuned
        # ------------------------------------------------------------------------------------------
        
        
        user.save()
        return user





# Restaurant Staff Account Creation
class RestaurantStaffRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    # restaurant_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Restaurant Name', 'class': 'form-control'}))
    # tin_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'TIN Number', 'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=CHOICES)
    # To Filter the restaurant_name exists in the Django User Model, get help from the following link:
    # https://stackoverflow.com/questions/27002564/django-queryset-is-it-possible-to-filter-for-field-is-null-for-floatfields/27002690
    restaurant = forms.ModelChoiceField(queryset=CustomUser.objects.filter(restaurant_name__isnull=False), empty_label='Select Your Restaurant')
    restaurant_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Restaurant ID', 'class': 'form-control'}))

    class Meta:
        # model = RestaurantStaff
        model = CustomUser
        # fields = ['email', 'first_name', 'last_name', 'gender', 'phone', 'restaurant', 'password1', 'password2']
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone', 'restaurant', 'restaurant_id', 'password1', 'password2']
        widgets = {
            'email' : forms.EmailInput(attrs = {'placeholder': 'Email', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RestaurantStaffRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].widget.attrs['class'] = 'form-control'
        self.fields['restaurant'].widget.attrs['class'] = 'form-control'
        # self.fields['restaurant'].widget.attrs['placeholder'] = 'Select Restaurant'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    
    # Override the save method of the restaurant-staff account creation.
    # Define the user-row as the restaurant-owner in the model
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        # user.restaurant_id = self.restaurant_id   # wanted to override the restaurant_id field in the backend with the value of the frontend's restaunrant_id.
        user.is_restaurant_staff = True
        # user.is_approved = False
        user.save()
        return user





# [ Further Development ]
# Anonymous user registration form. Might not be needed. It'll be a view for anonymous user registration, which only requires a view-url to get hit form the frontend, and an account will be registered for that anonymous user.
# Anonymous user login form. don't know if the anonymous user is registering without using email, how he/ she could login to the system. Will think later.





# Common User Login Form
class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # to hide the password-field-value while typing

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            
            # Raise auth-error where this form gets rendered
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials! Please insert correct email & password.")

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'