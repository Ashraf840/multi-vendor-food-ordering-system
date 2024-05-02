from django.db import models
from authentication.models import CustomUser
import string, random
from django.core.validators import MaxValueValidator, MinValueValidator   # Use to set range in the IntegerFields
from django.db import IntegrityError




# Food Tags Model (can be created by restaurant owner)
class Tag(models.Model):
    tag_name = models.CharField(max_length=50, blank=False, null=True, unique=True)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)  # store the restaurant-owner-id
    date_created = models.DateField(verbose_name='Date Created', auto_now_add=True)

    class Meta():
        verbose_name_plural = 'Food Tag'

    def __str__(self) -> str:
        return self.tag_name
    
    def save(self, *args, **kwargs):
        try:

            # [ FURTHER DEVELOPMENT ]: Make modification, cause duplicate-tag-name insertion is raising an error.
            # Make a query in the "Tag" table, to find if there is any duplicate tag already exist. 
            # try:
            # tagName_q = self.objects.get(tag_name=self.tag_name)
            # print(tagName_q)
            # if tagName_q is not None:

            # except:
            if self.tag_name is not None and self.tag_name[0] != '#':
                self.tag_name = '#' + self.tag_name


            # [ Reason for making this custom-condition ] If the restaurant-owner-staff forgets to create a tag-name without beginning with with a hash-tag,
            # then the system will automatically add a hash-tag by it's own.
        except IntegrityError:
            return print(IntegrityError)
        super(Tag, self).save(*args, **kwargs)





# Food Category Model (can be created by restaurant owner)
class Category(models.Model):
    cate_name = models.CharField(max_length=50, blank=False, null=True)
    # created_by = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='rest-owner+', verbose_name='Restaurant Owner')
    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    class Meta():
        verbose_name_plural = 'Food Category'

    def __str__(self) -> str:
        return self.cate_name






# Food Addons Model (can be created by restaurant owner)
class Addon(models.Model):
    addon_name = models.CharField(max_length=100, blank=False, null=True)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='rest-owner+', verbose_name='Restaurant Owner')
    price = models.FloatField()

    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    is_available = models.BooleanField(default=True)

    class Meta():
        verbose_name_plural = 'Food Addon'

    def __str__(self) -> str:
        return self.addon_name






# Food Code Generator ("Food" model)
# This method will generate a random-string of 8 chars.
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Food & Beverage Model (can be created by both restaurant owner)
class Food(models.Model):
    food_name = models.CharField(max_length=100, blank=False, null=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='category')
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='rest-owner+', verbose_name='Restaurant Owner')
    reward_point = models.PositiveSmallIntegerField(default=1)
    price = models.FloatField()
    food_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    tag = models.ManyToManyField(Tag, blank=True)
    addon = models.ManyToManyField(Addon, blank=True)
    image = models.FileField(upload_to='foodImage', default='foodImage/default_food_image.png', blank=True)
    total_viewed = models.PositiveBigIntegerField(default=0)
    # [ Further Development ] add "promo code" field. (default will be null, blank=true, make query from the "Promo Code" model for this restaurant). The model is in the "restaurantOwner" app.

    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    is_available = models.BooleanField(default=True)


    class Meta():
        verbose_name_plural = 'Food'

    def __str__(self) -> str:
        return self.food_name

    # Override the save-method of the model to generate food_code
    def save(self, *args, **kwargs):
        try:
            # [ Reasong for making this custom-condition ] Only generate food_code only while creating an instance of the food for the first time. 
            # Prohibit updating the food_code while updating any other field of that specific food-data-row.
            if self.food_name is not None and self.food_code is None:
                food_code_tuned = self.food_name.replace(" ", "_")
                self.food_code = food_code_tuned + "-" + random_string_generator()
        except:
            return True
        super(Food, self).save(*args, **kwargs)





# Food Rating (can be given by regular customers)
class FoodRating(models.Model):
    customer_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customer-id+', verbose_name='Customer')
    food_id = models.ForeignKey(to=Food, on_delete=models.CASCADE, related_name='food-id+', verbose_name='Food')
    # rating will be a range of 1-5. Ref:  https://www.py4u.net/discuss/149028
    rating = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)


    class Meta():
        verbose_name_plural = 'Food Rating (by Customer)'

    # def __str__(self) -> str:
    #     return self.food_name








# Food Review (can only be given by regular customers)
class FoodReview(models.Model):
    customer_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customer-id+', verbose_name='Customer')
    food_id = models.ForeignKey(to=Food, on_delete=models.CASCADE, related_name='food-id+', verbose_name='Food')
    # assign text-range in between 200 characters while in the forms of this model. 
    # Ref:  https://www.codegrepper.com/code-examples/python/django+text+area+limit+characters
    # Ref:  https://www.geeksforgeeks.org/textfield-django-models/
    review_msg = models.TextField(help_text='Write a review')
    
    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    # [ FURTHER DEVELOPMENT  ]
    # add 'hash-tags' fields

    class Meta():
        verbose_name_plural = 'Food Review (by Customer)'

    # def __str__(self) -> str:
    #     return self.food_name






# Food Review Helpful/ Not Helpful
class ReviewHelpful(models.Model):
    review_id = models.ForeignKey(to=FoodReview, on_delete=models.CASCADE, related_name='review-id+', verbose_name='Review')
    customer_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customer-id+', verbose_name='Customer')
    is_helpful = models.BooleanField(default=True)

    class Meta():
        verbose_name_plural = 'Food Review Helpful (Positive/ Negative)'







# Food Likes (can only be given by regular customers)
class FoodLikes(models.Model):
    customer_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customer-id+', verbose_name='Customer')
    food_id = models.ForeignKey(to=Food, on_delete=models.CASCADE, related_name='food-id+', verbose_name='Food')

    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    is_liked = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'Food Like'










# Food Likes (can only be given by regular customers)
class ComboMeal(models.Model):
    combo_name = models.CharField(verbose_name="Combo Meal Name", max_length=100, blank=False, null=True)
    RO_id = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='customer-id+', verbose_name='Restaurant')
    food_id = models.ManyToManyField(Food, blank=True)
    price = models.FloatField()

    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    is_available = models.BooleanField(default=True)

    class Meta():
        verbose_name_plural = 'Combo Meal'












