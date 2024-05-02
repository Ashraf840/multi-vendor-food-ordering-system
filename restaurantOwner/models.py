from django.db import models
import string, random
from authentication.models import CustomUser




def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))





class PromoCode(models.Model):
    promo_code_name = models.CharField(max_length=100, blank=False, null=True, unique=True)
    promo_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    rest_owner = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='rest-owner+', verbose_name='Restaurant Owner')
    discount_price = models.FloatField()

    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)

    is_available = models.BooleanField(default=True)

    class Meta():
        verbose_name_plural = 'Promo Code'

    def __str__(self) -> str:
        return self.promo_code_name


    def save(self, *args, **kwargs):
        try:
            # [ Reasong for making this custom-condition ] Only generate promo_code while creating an instance of the promo code for the first time. 
            # Prohibit updating the promo_code while updating any other field of that specific promo_code in the data-row.
            if self.promo_code_name is not None and self.promo_code is None:
                promo_code_tuned = self.promo_code_name.replace(" ", "_")
                self.promo_code = promo_code_tuned + "-" + random_string_generator()
        except:
            return True
        super(PromoCode, self).save(*args, **kwargs)



