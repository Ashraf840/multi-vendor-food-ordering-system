from django import forms
from django.db.models import fields
# from .models import *
from cartOrder.models import *


class AddtoCartForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['cart_id', 'food', 'quantity']

    # order_cancel = forms.BooleanField(
    #     required=False,
    #     label='Cancel Order',
    #     widget=forms.CheckboxInput(attrs={'checked': 'checked'}))

    # class Meta:
    #     model = Order
    #     fields = ['order_cancel']
    
    # def __init__(self, *args, **kwargs):
    #     super(OrderCancelForm, self).__init__(*args, **kwargs)
    #     self.fields['order_cancel'].widget.attrs['class'] = 'invisible'




# class OrderDeliveryDetailForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['delivery_time', 'delivery_address']

#     def __init__(self, *args, **kwargs):
#         super(OrderDeliveryDetailForm, self).__init__(*args, **kwargs)
#         self.fields['delivery_time'].widget.attrs['class'] = 'form-control'
#         self.fields['delivery_address'].widget.attrs['class'] = 'form-control'



# class PaymentMethodForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['payment_method']

#     def __init__(self, *args, **kwargs):
#         super(PaymentMethodForm, self).__init__(*args, **kwargs)
#         self.fields['payment_method'].widget.attrs['class'] = 'form-control'