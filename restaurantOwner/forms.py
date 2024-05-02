from django import forms
from django.db.models import fields
from .models import *




# Food Addon Form
class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['promo_code_name', 'discount_price']

    def __init__(self, *args, **kwargs):
        super(PromoCodeForm, self).__init__(*args, **kwargs)
        self.fields['promo_code_name'].widget.attrs['class'] = 'form-control text-white'
        self.fields['promo_code_name'].widget.attrs['placeholder'] = 'Create food addon'
        self.fields['discount_price'].widget.attrs['class'] = 'form-control text-white'
        self.fields['discount_price'].widget.attrs['placeholder'] = '৳ 0.00'

        # Custom Form-field Attributes (especially for "id" & "style" attributes, but can be used for abyother attributes like "class" etc)
        # Helper Link:  https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
        self.fields['promo_code_name'].widget.attrs.update({
            'id':'promo-code-name-update',
            'style': 'padding: .8rem .6rem; background-color: #343a40;',
        })
        self.fields['discount_price'].widget.attrs.update({
            'id':'promo_code-discount-price-update',
            'style': 'padding: .8rem .8rem; background-color: #343a40;',
        })


