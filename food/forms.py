from django import forms
from django.db.models import fields
from .models import *



# Food Tag Form
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_name']

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['tag_name'].widget.attrs['class'] = 'form-control text-white'
        self.fields['tag_name'].widget.attrs['placeholder'] = 'Add food tag name'
        
        # Custom Form-field Attributes (especially for "id" & "style" attributes, but can be used for abyother attributes like "class" etc)
        # Helper Link:  https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
        self.fields['tag_name'].widget.attrs.update({
            'id':'tag-name-update',
            'style': 'border-radius: 5px 0 0 5px; padding: .8rem .6rem; background-color: #343a40;',
        })





# Food Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['cate_name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['cate_name'].widget.attrs['class'] = 'form-control text-white'
        self.fields['cate_name'].widget.attrs['placeholder'] = 'Add food category'

        # Custom Form-field Attributes (especially for "id" & "style" attributes, but can be used for abyother attributes like "class" etc)
        # Helper Link:  https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
        self.fields['cate_name'].widget.attrs.update({
            'id':'food-category-name-update',
            'style': 'border-radius: 5px 0 0 5px; padding: .8rem .6rem; background-color: #343a40;',
        })





# Food Addon Form
class AddonForm(forms.ModelForm):
    class Meta:
        model = Addon
        fields = ['addon_name', 'price']

    def __init__(self, *args, **kwargs):
        super(AddonForm, self).__init__(*args, **kwargs)
        self.fields['addon_name'].widget.attrs['class'] = 'form-control text-white'
        self.fields['addon_name'].widget.attrs['placeholder'] = 'Create food addon'
        self.fields['price'].widget.attrs['class'] = 'form-control text-white'
        self.fields['price'].widget.attrs['placeholder'] = '৳ 0.00'

        # Custom Form-field Attributes (especially for "id" & "style" attributes, but can be used for abyother attributes like "class" etc)
        # Helper Link:  https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
        self.fields['addon_name'].widget.attrs.update({
            'id':'food-addon-name-update',
            'style': 'padding: .8rem .6rem; background-color: #343a40;',
        })
        self.fields['price'].widget.attrs.update({
            'id':'food-addon-price-update',
            'style': 'padding: .8rem .8rem; background-color: #343a40;',
        })





# Food Form
class FoodForm(forms.ModelForm):
    # food_name = forms.CharField(label='Food Name:', widget=forms.TextInput(attrs={'placeholder': 'Enter food name'}))
    # email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    # message = forms.TextField(label='Message', widget=forms.TextInput(attrs={'placeholder': 'Message'}))
    # category = forms.ModelChoiceField(label="Placeholder")
    category=forms.ModelChoiceField(label="", queryset=Category.objects.all().distinct(), empty_label="Select a category")
    class Meta:
        model = Food
        fields = ['food_name', 'category', 'reward_point', 'price', 'tag', 'addon', 'image']

    def __init__(self, *args, **kwargs):
        # self._pwd = kwargs.pop('pwd', None)
        # particular_rest_cate = kwargs.get('food_category')
        # print('Initial Food Category: %s' % particular_rest_cate)
        
        super(FoodForm, self).__init__(*args, **kwargs)

        # Get the category of the specific restaurant
        # Get the inital values set in the view


        self.fields['food_name'].widget.attrs['class'] = 'form-control'


        self.fields['category'].widget.attrs['class'] = 'form-control'
        # self.fields['category'].queryset = Category.objects.filter(category=particular_rest_cate).all()
        # food_category
        
        self.fields['reward_point'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['tag'].widget.attrs['class'] = 'form-control'
        self.fields['addon'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'


        self.fields['food_name'].widget.attrs.update({
            'placeholder':'Enter food name',
        })

        self.fields['price'].widget.attrs.update({
            'placeholder':'৳ 0.00',
        })








    # def createFood(self):
    #     name = self.cleaned_data.get('first_name')
    #     username = self.cleaned_data.get('email')
    #     to_email = self.cleaned_data.get('email')
    #     password1 = self._pwd






        # u_id = self.user.id
        # # food_category = Category.objects.filter(
        # #     Q(created_by=u_id)
        # # ).all()
        # print('U-ID: %s' % u_id)
        
        # self.fields['addon_name'].widget.attrs['placeholder'] = 'Create food addon'
        # self.fields['price'].widget.attrs['class'] = 'form-control text-dark'
        # self.fields['price'].widget.attrs['placeholder'] = '৳ 0.00'

        # # Custom Form-field Attributes (especially for "id" & "style" attributes, but can be used for abyother attributes like "class" etc)
        # # Helper Link:  https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
        # self.fields['addon_name'].widget.attrs.update({
        #     'id':'food-addon-name-update',
        #     'style': 'padding: .8rem .6rem; background-color: #343a40;',
        # })
        # self.fields['price'].widget.attrs.update({
        #     'id':'food-addon-price-update',
        #     'style': 'padding: .8rem .8rem; background-color: #343a40;',
        # })






# Food Form (only food-image field)
class FoodImageForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(FoodImageForm, self).__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['class'] = 'form-control'

        self.fields['image'].widget.attrs.update({
            'id':'custom-file-upload-btn',
        })

