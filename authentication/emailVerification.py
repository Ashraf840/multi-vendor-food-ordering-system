# Email Verification Setup Libraries
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views import View
import threading

from .models import CustomUser
from django.contrib import messages
from django.shortcuts import redirect








# Multi-threading; Email will be sent faster & the user will not feel like waiting to be redirected to the login page
class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.email = msg
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



def emailVerification(user_id, req_dict_domain, user, user_email, fullName):
    # Setup for sending email activation code via HTML template for Email (which is inside the 'authentication/rest_staff_accnt_activation_email_template' folder).
    uidb64 = urlsafe_base64_encode(force_bytes(user_id))
    domain = get_current_site(req_dict_domain).domain       #  "http://127.0.0.1:8000"

    # Inside the token_generator of "utils.py", encoded the "user.is_active=Ture"
    # "userAuth:activate" is the "User Account Activation" endpoint of the 'urls.py' file
    link = reverse('userAuth:activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})    

    activate_url = 'http://'+domain+link

    email_subject = 'Activate you account - Food Recommendation System'
    from_email = 'python4dia@gmail.com'
    to_email = user_email

    context = { 'username': fullName, 'activate_url':activate_url, }

    # Email templates; will be rendered then sent 
    text_content = render_to_string('authentication/rest_staff_accnt_activation_email_template/account_activation.txt', context)
    html_content = render_to_string('authentication/rest_staff_accnt_activation_email_template/account_activation.html', context)

    # Pass the rendered_string_email_template inside the 'EmailMultiAlternatives' method (initialize the object) & store it into a variable, then lastly call the 'send()' method to send the 'msg' via email.
    msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    # msg.send()
    EmailThread(msg).start()    # sends email, while the user is redirected to the login page without being awaited for send finishing the mail-sending-process.









# Redirection link to the login page after user-account activation
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            # check_token: Check that an account activation token is correct for a given user. Simply checks if the token is already been used or not
            if not token_generator.check_token(user, token):
                messages.warning(request, 'Your account is already activated.')
                return redirect('userAuth:login')

            if user.is_active:
                return redirect('userAuth:login')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Account activated successfully')
                return redirect('userAuth:login')
        except Exception as ex:
            pass

