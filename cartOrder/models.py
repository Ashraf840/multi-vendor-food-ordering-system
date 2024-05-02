from django.db import models
from authentication.models import CustomUser
from food.models import Food
import string, random



# ------------------------------
# "S I G N A L S" included
# ------------------------------



# Models-class: Order
# This method will generate a random-string of 20 chars.
def random_string_generator(size=20, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Cart (can only be created by customers)
# [ Further Item ]:  generate a cart using signals, while a customer added a food-item inside the "CartItem" model.
# [ Important Note ]:  This cart will be deleted, whenever a customer enters into another restaurant-page for ordering foods from that restaurant.
class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer+', verbose_name='Customer')  # store the customer-id
    is_ordered = models.BooleanField(default=False)
    cart_id = models.CharField(max_length=100, blank=True)      # auto-generated via overriding the "save" method of this model
    total_cart_items = models.PositiveBigIntegerField(default=0)    # signal ("update_price") is used
    total_price = models.FloatField(default=0)  # signal ("update_price") is used
    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)
    restaurant = models.CharField(max_length=150, blank=True, null=True)

    class Meta():
        verbose_name_plural = 'Shopping Cart'

    # def __str__(self) -> str:
    #     return (str(self.id) + '_' 
    #         + str(self.customer.first_name) + '_' 
    #         + str(self.customer.last_name))
    def __str__(self) -> str:
        return self.cart_id

    # overriding the 'save' method to generate random-string while creating an cart-record using the "random_string_generator" method.
    def save(self, *args, **kwargs):
        # If no 'cart_id' isn't passed while creating an order.
        if not len(self.cart_id):
            self.cart_id = str(self.customer) + "_" + random_string_generator()
        super(Cart, self).save(*args, **kwargs)










# Cart-item (will store multiple food-items which will be defined by specific cart)
class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)  # store the cart-instance
    # customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer+', verbose_name='Customer')  # required for the signals to calculate the total cart item of the customer for th e current cart
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='food+', verbose_name='Food')  # store the food-id
    cartItem_id = models.CharField(max_length=100, blank=True)      # auto-generated via "save" method
    price = models.FloatField(default=0)    # signal ("update_price") is used
    quantity = models.PositiveBigIntegerField(default=1)
    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)
    # create another field ("is_ordered"), it'll be updated whenever the cart proceed to checkout. *****************
    # is_ordered = models.BooleanField(default=False)


    class Meta():
        verbose_name_plural = 'Shopping Cart Items'

    # def __str__(self) -> str:
    #     return (str(self.id) + '_' 
    #         + str(self.cart) + '_' 
    #         + str(self.food.food_name) + '_' 
    #         + str(self.customer.first_name))
    # def __str__(self) -> str:
    #     return self.customer
    def __str__(self) -> str:
        return self.cartItem_id

    # overriding 'save' method to generate random-string while creating an order-record using the "random_string_generator" method
    def save(self, *args, **kwargs):
        # If no 'cartItem_id' isn't passed while creating an order.
        if not len(self.cartItem_id):
            self.cartItem_id = str(self.food) + "_" + random_string_generator()
        super(CartItem, self).save(*args, **kwargs)









# Create "Order" model
PAYMENT_CHOICES = [
    ('COD', 'COD'),
    ('SSLCommerz', 'SSLCommerz'),
]

ORDER_STATUS_CHOICES = [
    ('Order Received by Restaurant', 'Order Received by Restaurant'),
    ('Baking', 'Baking'),
    ('Baked', 'Baked'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Order Received by Customer', 'Order Received by Customer'),
]
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer+', verbose_name='Customer')  # store the customer-instance
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)  # store the cart-instance
    price = models.FloatField(default=0)    # "total_price" of the "Cart" model
    payment_method = models.CharField(verbose_name='Payment Method', max_length=20, choices=PAYMENT_CHOICES, default='COD')
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    delivery_address = models.TextField(verbose_name="Delivery Address")
    delivery_time = models.DateField(verbose_name='Delivery Time', auto_now_add=True)
    order_id = models.CharField(verbose_name='Order ID', max_length=100)    # will be auto-generated via overriding the 'save' method
    order_num = models.CharField(verbose_name='Order Number', max_length=100)    # will be auto-generated via overriding the 'save' method
    restaurant = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateField(verbose_name='Date Created', auto_now_add=True)
    last_updated_at = models.DateField(verbose_name='Last Updated', auto_now_add=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Order Received by Restaurant')

    class Meta:
        verbose_name_plural = "Order"
    
    def __str__(self) -> str:
        return self.order_id

    # overriding 'save' method to generate random-string while creating an order-record using the "random_string_generator" method
    def save(self, *args, **kwargs):
        # If no 'order_id' isn't passed while creating an order.
        if not len(self.order_id):
            self.order_id = str(self.customer) + "_" + str(self.cart_id) + "_"  + random_string_generator()
        
        if not len(self.order_num):
            self.order_num = str(self.customer) + "_"  + random_string_generator()
        super(Order, self).save(*args, **kwargs)



    # THIS METHOD IS USED BY THE CONSUMER ("OrderProgress"), whenever any frontend-websocket connection is made with this "OrderProgress" consumer, it initially makes the order-table query from the DB to serve the frontend-websocket with the initial data of that specific order (order_id).
    # give the order-id as param whenever this-model-class-method is called & get the order-details.
    # used in the 'consumers.py' to get the current info of that specific-order.
    # The func is used inside the 'consumers.py' file's 'connect()' func.   *****************
    # Whenever this func gets called, it'll return the specific order-data by making query.
    # THIS METHOD SERVES THE SPECIFIC ORDER RECORD.
    @staticmethod
    def get_order_detail(order_id):
        instance = Order.objects.filter(order_id=order_id).first()
        
        print('"Order" model staticmethod is called')
        print('"Order" model staticmethod - Order Instance: ', instance)
        print('"Order" model staticmethod - Order Instance: ', instance.price)
        
        data = {
            'order_id': instance.order_id,
            'price': float(instance.price),   # the Decimal type is not able to be serialized directly into JSON.
            'status': instance.status,
            'is_paid': instance.is_paid,
            'is_cancelled': instance.is_cancelled,
        }

        # Make a progress-percentage based on the 5-types of order-status
        progress_percentage = 0
        if instance.status == 'Order Received by Restaurant':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for Delivery':
            progress_percentage = 80
        elif instance.status == 'Order Received by Customer':
            progress_percentage = 100
        
        data['progress'] = progress_percentage  # extending the data-dict, which will also be used in the consumer-class ("OrderProgress")

        return data








# [ Not sure ] Create the "payment-method" model inside the "userProfile" application, then called inside the order-model


