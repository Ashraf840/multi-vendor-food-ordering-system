from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, RestaurantOwnerRegistrationForm , RestaurantStaffRegistrationForm
from .decorators import *
# from django.contrib.auth.decorators import login_required
from .models import CustomUser
# from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# Email Verification Custom Function import
from .emailVerification import emailVerification





# >>>>>>>>>>>>>>>>>>>>>>> Use Signals.py to make sure any user-type registration an default inactive account. 
# But the "signals.py" file needs to be imported inside the 'apps.py' file
# Enabled one-time-use tokenized email verification
# Mail will later be sent to the user-email-account using the threading technology, since it will redirect the user to the login page, while the mail gets sent simultaneously



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Email verification function (custom-made) & EmailTreading is being shifted to the 'foodsystem/authentication/emailVerification.py'
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




# >>>>>>>>>>>>>>>>>>>> Regular User (Customer) Registration

@stop_authenticated_users
def userReg(request):
    context = {
        'title': 'User Registration',
    }
    # if request.method == 'POST':
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # By saving the form, django is committing that form-data inside the DB
            user = form.save()

            # Email Verification scattered codes are written inside a func ('emailVerification'), which is later shifter in a separate file 'foodsystem/authentication/emailVerification.py'.
            # Get the full name of the user
            firstName = form.cleaned_data.get('first_name')
            lastName = form.cleaned_data.get('last_name')
            fullName = firstName + ' ' + lastName   # This value will be sent along with the email body


            user_id = user.pk
            req_dict_domain = request   #domain of the current url of the browser
            user = user
            user_email = user.email
            fullName = fullName
            # Then complete raw code to send "Email Verification Token" in written in a function, then this function will be called from a different file "emailVerification.py".
            emailVerification(user_id=user_id, req_dict_domain=req_dict_domain, user=user, user_email=user_email, fullName=fullName)

            messages.info(request, "Congratulation %s! You're account has been created successfully!" % (fullName)) # This msg will be shown in the login-page since the user-account is created successfully & the user will be redirected to the login-page.
            messages.info(request, "Please check your email for activation")
            return redirect('userAuth:login')

        # If error occurs, display the form as empty again
        else:
            # Helpful Ref: Check the error message if the form doesn't appropriately save to the db-model in the backend
            # https://stackoverflow.com/questions/46639971/django-form-doesnt-runs-form-is-valid
            # Added else statment
            msg = 'Errors: %s' % form.errors.as_text()
            context['registerForm'] = form
            # Show the empty login-form again, if invalid credentials are inserted
            messages.info(request, '%s' % msg)

    # Get req
    else:
        form = UserRegistrationForm()   # display empty form while tha page gets loaded
        context['registerForm'] = form
    
    return render(request, 'authentication/regForm.html', context)





# ------------------------------------------------------
# [ Further Development ]
# Anonymous user registration form. Might not be needed. It'll be a view for anonymous user registration, which only requires a view-url to get hit form the frontend, and an account will be registered for that anonymous user.
# Anonymous user login form. don't know if the anonymous user is registering without using email, how he/ she could login to the system. Will think later.
# ------------------------------------------------------






# >>>>>>>>>>>>>>>>>>>> Restaurant Owner Registration

@stop_authenticated_users
def restaurantOwnerReg(request):
    context = {
        'title': 'Restaurant Owner Registration',
    }
    # if request.method == 'POST':
    if request.POST:
        print(request.POST.dict())

        form = RestaurantOwnerRegistrationForm(request.POST)
        if form.is_valid():
            # By saving the form, django is committing that form-data inside the DB
            user = form.save()

            # Email Verification scattered codes are written inside a func ('emailVerification'), which is later shift in a separate file 'foodsystem/authentication/emailVerification.py'.
            # Get the full name of the user
            firstName = form.cleaned_data.get('first_name')
            lastName = form.cleaned_data.get('last_name')
            fullName = firstName + ' ' + lastName   # This value will be sent along with the email body


            user_id = user.pk
            req_dict_domain = request   #domain of the current url of the browser
            user = user
            user_email = user.email
            fullName = fullName
            # Then complete raw code to send "Email Verification Token" in written in a function, then this function will be called from a different file "emailVerification.py".
            emailVerification(user_id=user_id, req_dict_domain=req_dict_domain, user=user, user_email=user_email, fullName=fullName)

            messages.info(request, "Successfully created an account for %s as a restaurant owner!" % (fullName)) # This msg will be shown in the login-page since the user-account is created successfully & the user will be redirected to the login-page.
            messages.info(request, "Please check your email for activation")
            return redirect('userAuth:login')

        # If error occurs, display the form as empty again
        else:
            # Helpful Ref: Check the error message if the form doesn't appropriately save to the db-model in the backend
            # https://stackoverflow.com/questions/46639971/django-form-doesnt-runs-form-is-valid
            # Added else statment
            msg = 'Errors: %s' % form.errors.as_text()
            context['registerForm'] = form
            # Show the empty login-form again, if invalid credentials are inserted
            messages.info(request, '%s' % msg)
            # return HttpResponse(msg, status=400)
    # Get req
    else:
        form = RestaurantOwnerRegistrationForm()   # display empty form while tha page gets loaded
        context['registerForm'] = form
    
    return render(request, 'authentication/regForm-restaurant-owner.html', context)





# >>>>>>>>>>>>>>>>>>>> Restaurant Staff Registration

@stop_authenticated_users
def restaurantStaffReg(request):
    context = {
        'title': 'Restaurant Staff Registration',
    }

    # if request.method == 'POST':
    if request.POST:
        form = RestaurantStaffRegistrationForm(request.POST)

        # Can attain any form-input-value by using the "get()" method
        restaurant_id = request.POST.get('restaurant_id')
        print('%s Restaurant Frontend ID: %s %s' % ( ('*'*10), (restaurant_id), ('*'*10) ))

        # Fetch the row of that specific restaurant
        print(request.POST.dict())

        # Check if the restaurant_id exists in the "RestaurantOwner" table in the DB
        # allUser=get_user_model()
        # checker_restaurant_id = allUser.objects.filter(restaurant_id=restaurant_id).first()


        # Fetch the entire user-data-row from the custom-user-table from the backend DB
        checker_restaurant_id = CustomUser.objects.filter(restaurant_id=restaurant_id).first()


        # if restaurant_id exists in the DB table
        if checker_restaurant_id is not None:
            print('Restaurant is found in the DB!')
            print(checker_restaurant_id.restaurant_id)  # getting the restaurant_id from the backend

            # Viewing the value of frontend & backend restaurant_id
            # backend_restaurant_id = checker_restaurant_id.restaurant_id
            # print('%s Restaurant ID (Backend): %s %s' % ( ('*'*10), (backend_restaurant_id), ('*'*10) ))
            # print('%s Restaurant ID (Frontend): %s %s' % ( ('*'*10), (frontend_restaurant_id), ('*'*10) ))


            restaurant_id_post = request.POST.get('restaurant_id')
            restaurant = CustomUser.objects.filter(restaurant_id=restaurant_id_post).first() # Fetched the specific data-row of that "CustomUser" table
            print('%s Restaurant Name: %s %s' % ( ('*'*10), (restaurant), ('*'*10) ))

            # Store the backend restaurant-id in a variable.
            backend_restaurant_id = restaurant.restaurant_id
            frontend_restaurant_id = request.POST.get('restaurant_id')

            print('%s Restaurant ID (Backend): %s %s' % ( ('*'*10), (backend_restaurant_id), ('*'*10) ))
            print('%s Restaurant ID (Frontend): %s %s' % ( ('*'*10), (frontend_restaurant_id), ('*'*10) ))

            # Check whether the restaurant-id is matched based on the SELECTED RESTAURANT and the id provided by the new restaurant-staff.
            if backend_restaurant_id == frontend_restaurant_id:
                # messages.info(request, "Successfully created an account for the restaurant staff!") # This msg will be shown in the login-page since the user-account is created successfully & the user will be redirected to the login-page.
                print('%s Restaurant id is matched (with the selected Restaurant\'s actual ID)! %s' % ( ('*'*10), ('*'*10) ))


                if form.is_valid():
                    # Helpful Ref: How to make a specific field assigned to the according field of the backend's model
                    # https://stackoverflow.com/questions/22739701/django-save-modelform
                    # Although, it's not necessary here. requirement attained by using the default model-field explicitly in the 'RestaurantStaffRegistrationForm' as the field of 'restaurant_id'
                    # restaurant_staff_form = form.save(commit=False)
                    # # commit=False tells Django that "Don't send this to database yet.
                    # # I have more things I want to do with it."
                    # restaurant_staff_form.restaurant_id = frontend_restaurant_id # Set the user object here
                    # print(restaurant_staff_form)
                    # restaurant_staff_form.save() # Now you can send it to DB

                    # By saving the form, django is committing that form-data inside the DB
                    user = form.save()

                    # Email Verification scattered codes are written inside a func ('emailVerification'), which is later shifter in a separate file 'foodsystem/authentication/emailVerification.py'.
                    # Get the full name of the user
                    firstName = form.cleaned_data.get('first_name')
                    lastName = form.cleaned_data.get('last_name')
                    fullName = firstName + ' ' + lastName   # This value will be sent along with the email body


                    user_id = user.pk
                    req_dict_domain = request
                    user = user
                    user_email = user.email
                    fullName = fullName
                    # Then complete raw code to send "Email Verification Token" in written in a function, then this function will be called from a different file "emailVerification.py".
                    emailVerification(user_id=user_id, req_dict_domain=req_dict_domain, user=user, user_email=user_email, fullName=fullName)


                    messages.info(request, "Successfully created an account for %s as a restaurant staff!" % (fullName)) # This msg will be shown in the login-page since the user-account is created successfully & the user will be redirected to the login-page.
                    messages.info(request, "Please check your email for activation")
                    return redirect('userAuth:login')
                else:
                    # Helpful Ref: Check the error message if the form doesn't appropriately save to the db-model in the backend
                    # https://stackoverflow.com/questions/46639971/django-form-doesnt-runs-form-is-valid
                    # Added else statment
                    msg = 'Errors: %s' % form.errors.as_text()
                    messages.info(request, '%s' % msg)
                    form = RestaurantStaffRegistrationForm()
                    context['registerForm'] = form
                    # return HttpResponse(msg, status=400)
            else:
                print('%s Restaurant id didn\'t matched (with the selected Restaurant\'s actual ID)! %s' % ( ('*'*10), ('*'*10) ))
                messages.info(request, "Invalid restaurant-id! Please enter the restaurant-id correctly!")
                return redirect('userAuth:registrationRestStaff')
                # redirect to the register page, with the msg "Incorrect restaurant id, not matched"
                
                # [ FURTHER DEVELOPMENT ]
                # Display the attempt-count to the redirected-staff-register page.
                # After 3 attemps, block the user-IP for 1 hour.

        else:
            print('Restaurant is not found in the DB!')
            messages.info(request, "Please enter the restaurant-id correctly! Restaurant id is not found in the DB!")
            return redirect('userAuth:registrationRestStaff')
            # Redirect the user to the register page with the msg to enter the restaurant-id correctly.

            # [ FURTHER DEVELOPMENT ]
            # Display the attempt count in the redirected-staff-register page.
            # After 3 attemps, block the user-IP for 1 hour.


        # Obsolete [not using]
        # If any error (password1 & password2 didn't matched) occurs, display the empty form again
        # context['registerForm'] = form
        # Show the empty login-form again, if invalid credentials (password1 & password2) are inserted
        # messages.info(request, 'Wrong Password!')

    # Get request
    else:
        form = RestaurantStaffRegistrationForm()   # display empty form while tha page gets loaded
        context['registerForm'] = form
    
    return render(request, 'authentication/regForm-restaurant-staff.html', context)









# >>>>>>>>>>>>>>>>>>>> Common User Login Function (for the system admins, restaurant owner & staff, regular customer)

@stop_authenticated_users
def userLogin(request):
    context = {
        'title': 'User Login',
    }

    # [GET req] Render the form while the page loads
    form = UserLoginForm()
    context['loginForm'] = UserLoginForm()

    # [POST req]
    if request.POST:
        form = UserLoginForm(request.POST)
        
        # NB: shifted the variables from the 'form.is_valid()' code-block, these variables-values will be used in the else-code-block also
        email = request.POST['email']
        password = request.POST['password']
        
        if form.is_valid():




            
            # [ PROBLEM ]: If I try to login using an unknown email, then it returns an error.
            try:
                user = CustomUser.objects.filter(email=email)
                print(user)
                if user:
                # if get_object_or_404(CustomUser, email=email):
                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        # # Route regular users and restaurant-staffs differently
                        # if user.is_superuser or user.is_admin or user.is_staff:
                        #     return redirect('restaurantStaffApplication:home_restaurant_staffs')
                        # else:
                        #     return redirect('homeApplication:homepage')



                        # Route the admin, customer, restaurant owner, restaurant staff to different home-page
                        # Redirecting system-admins & system-staffs to their homepage (OK)
                        # [Later Development]:  after login, redirect the user to his/her respective homepages
                        if user.is_superuser or user.is_admin or user.is_staff:
                            return render(request, 'testing_auth/system_admin.html', context)
                        # Redirecting restaurant-owners to their homepage
                        elif user.is_restaurant_owner:
                            # return render(request, 'testing_auth/restaurant_owner.html', context)
                            # return render(request, 'restaurantOwner/homepage.html', context)
                            return redirect('restaurantOwnerApplication:rowner_homepage')
                        # Redirecting restaurant-staffs to their homepage
                        elif user.is_restaurant_staff:
                            # [Further Development]
                            # Check if the staff is active/ inactive
                            if user.is_approved:
                                # return render(request, 'testing_auth/restaurant_staff.html', context)
                                return redirect('restaurantStaffApplication:rstaff_homepage')
                            else:
                                # [ Futher Development ]: Add flash-msg while redirected to the pending staff's homepage
                                # msg = 'Please wait till your restaurant owner approve your account.'
                                # messages.info(request, '%s' % msg)
                                # return redirect('userAuth:res_staff_unapproved_homepage')
                                # return render(request, 'testing_auth/restaurant_staff_unapproved.html', context)
                                
                                # [ MAKE A VIEW IN THE 'restaurantStaff' app, which will render the following page. Inside that view, the restaurant-owner & other staffs will be displayed querying from the backend ]
                                # return render(request, 'restaurantStaff/restaurant_staff_unapproved.html', context)
                                return redirect('restStaffApp:rstaff_homepage_unapproved')
                        # Redirecting regular customers to their homepage
                        elif user.is_regular_user:
                            # return render(request, 'testing_auth/customer.html', context)
                            return redirect('restCustApp:rcust_homepage')
                        # Redirecting anonymous users to their homepage
                        elif user.is_anonymous_user:
                            return render(request, 'testing_auth/anonymous_customer.html', context)
                        else:
                            msg = 'Login unsuccessful with unknown reason.'
                            messages.info(request, '%s' % msg)
                            return redirect('userAuth:login')
                else:
                    # [ Pass a request.message ] 
                    msg = 'Enter a correct email address!'
                    messages.info(request, '%s' % msg)
                    return redirect('userAuth:login')
                
            except user.DoesNotExist:
                msg = 'Login unsuccessful!'
                messages.info(request, '%s' % msg)
                return redirect('userAuth:login')




        else:
            # Check if the requested user is active/ not, querying from the backend DB
            # fetch the data record from the DB of the specific user using the email inserted as input for login purpose.
            try:
                user_detail = CustomUser.objects.get(email=email)
                print('User account active status: %s' % user_detail.is_active)
                if user_detail.is_active == False:
                    msg = 'Please verify your email to activate your account.'
                else:
                    msg = 'Errors: %s' % form.errors.as_text()
            except:
                msg = 'Errors: Invalid Credentials!'
                messages.info(request, '%s' % msg)
                return redirect('userAuth:login')

            # return HttpResponse(msg, status=400)

            # Show the empty login-form again, if invalid credentials are inserted
            messages.info(request, '%s' % msg)
            # print("Invalid Credentials! %s" % ('*'*20))
            return redirect('userAuth:login')

    return render(request, 'authentication/loginForm.html', context)






# @login_required(login_url='userAuth:login')
def userLogout(request):
    logout(request)
    return redirect('userAuth:login')
