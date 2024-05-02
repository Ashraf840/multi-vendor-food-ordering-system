from django import forms
from django.db.models import fields
from .models import *



# ----------------------------------------------------------------
# This form will be used by the restaurant-owner & restaurant-staff
# ----------------------------------------------------------------

class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(OrderStatusUpdateForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'
