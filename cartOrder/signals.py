from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import *
from food.models import Food
from django.db.models import Q


# Dj Channels
from channels.layers import get_channel_layer   # to get all the channel-layers
from asgiref.sync import async_to_sync
import json


# from asgiref.sync import sync_to_async
# import asyncio
# import aiohttp
# from channels.db import database_sync_to_async


# # **************** Write another signal, to update the cart-items "is_ordered" to True, 
# # whenever the customer proceed to the checkout with the cart-instance.


# # @sync_to_async
# @database_sync_to_async
# def update_cart_items(cit):
# # async def update_cart_items(cit):
# # def update_cart_items(cit):
#     # while cit.is_ordered == False:

#     cit.is_ordered = True
#     print(cit.is_ordered)
    
#     cit.save()
#     # pass


    # async with aiohttp.CLientSession() as client:
    #     tasks = []
    #     for ct in cit:
    #         task = asyncio.ensure_future(cit.save())
    #         tasks.append(task)
    #     await asyncio.gather(*tasks)





# @receiver(pre_save, sender=Cart)
# # @receiver(post_save, sender=Cart)
# def update_cart_item_ordered_bool(sender, **kwargs):
# # async def update_cart_item_ordered_bool(sender, **kwargs):
#     # Fetch all the cart-items of this particular cart
#     cart = kwargs['instance']
#     # print(cart)
#     cart_items = CartItem.objects.filter(
#         Q(cart=cart)
#         & Q(is_ordered=False)
#     ).all()


#     # print('*' * 10)
#     # print(cart_items)
#     # print('*' * 10)

#     # Check if any "CartItem" field "is_ordered" is True, if True, then don't proceed to make the respective cart-items "is_ordered" is "True"
#     # [ Double Validation ]
#     # proceed = True

#     # Check if the field "is_ordered" = False of the "Cart" instance
#     for cit in cart_items:
#     #     # if cit.is_ordered == False:
#         # cit.is_ordered = True
#     # #         # proceed = False
#     #     print(cit.is_ordered)
#         # cit.save()
#         # update_cart_items(cit)
#         # await update_cart_items(cit)
#     # asyncio.create_task(update_cart_items(cit))
#     # asyncio.wait(update_cart_items)
        
#         task = asyncio.ensure_future(update_cart_items(cit))
#         await asyncio.wait(task)
#     # await asyncio.run(task)


# # if __name__ == "__main__":
# #     asyncio.run(update_cart_items())

# # if __name__ == "__main__":
# #     asyncio.run(update_cart_item_ordered_bool())





# Signals for "CartItem" model (increase the price based on the food-quantity; also update the corresponding cart's "total_quantity & total_price" field)
@receiver(pre_save, sender=CartItem)
def update_price(sender, **kwargs):
    print('*'*10)
    print('"update_price" signal is called!')
    print('*'*10)

    # print the whole instance of the "CartItem" db-model
    # print(kwargs)
    # print(kwargs['instance'])
    


    # Get the "CartItems" through the kwargs, everytime an cart-item is created.
    cart_items = kwargs['instance']
    # fetch the food-instance from the "Food" db-model
    price_of_food = Food.objects.get(id=cart_items.food.id)
    # print(price_of_food)
    # print(cart_items.quantity)
    # print(price_of_food.price)
    # total_items_price = cart_items.quantity * price_of_food.price

    # set the total price into the field "price" in the "CartItem" db model
    cart_items.price = cart_items.quantity * price_of_food.price
    # print(cart_items.price)

    
    # print('*'*10)
    # # print(cart_items.customer)
    # print(cart_items.cart_id)
    # print('*'*10)

    
    # Get the total cart items
    # total_cart_items = CartItem.objects.filter(customer=cart_items.customer).all()
    total_cart_items = CartItem.objects.filter(cart_id=cart_items.cart_id).all()
    # print('*' * 10)
    # print(len(total_cart_items) + 1)
    # print('*' * 10)


    # cart_items.price = total_items_price

    
    # cart_items.quantity = len(total_cart_items) + 1
    

    # cart_items.save()


    # print(cart_items.customer)
    # total_cart_items = CartItem.objects.filter(customer=cart_items.customer.id)
    # print(total_cart_items)
    # cart_items.quantity = total_cart_items.count()
    # print('Quantity: %s' % cart_items.quantity)

    # # Update the "total_price" of a "Cart" instance
    # print(cart_items.id)

    # Update the total price of the "Cart" db model
    # print(cart_items.cart.id)
    # print(cart_items.cart)



    # [ Update the respective "Cart" model's total-item, total-price fields accordingly ]
    # First fetch the total-quantity & total-price of all the cart items of the customer, 
    # then set the total_quantity & total_price accordingly into the fields of "total_quantity" & "total_price" in the "Cart" of db model.
    
    # cart = Cart.objects.get(id=cart_items.cart.id)
    cart = Cart.objects.get(cart_id=cart_items.cart_id.cart_id)
    print('Total Price: %s' % cart.total_price)
    cart.total_cart_items = len(total_cart_items) + 1
    cart.total_price += cart_items.price
    cart.save()







# Signals for "CartItem" model (increase the price based on the food-quantity)
# @receiver(pre_save, sender=CartItem)
# def update_price_for_foodRemove(sender, **kwargs):
#     print('*'*10)
#     print('A food-item is removed! Signal: "update_price_for_foodRemove"')
#     print('*'*10)
#     pass






# Signals for food-order-status [ Django-channels ]
# Enable the functionality of real-time order-status-updation to the django-consumer ('OrderProgress')
# Post-save signal for Order-model-class using Consumer/ Websocket
# Only works for [ ORDER-UPDATION ]
@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    # If no new record is created, means the old records are updated/ modified, then execute the next block of code.
    # 'sender' is the order-model-class & 'instance' is the individual-order-record.
    if not created:
        # This customized data-dict will be sent to the frontend-websocket
        data = {
            'order_id': instance.order_id,
            'price': float(instance.price),   # the Decimal type is not able to be serialized directly into JSON.
            'status': instance.status,
            'is_paid': instance.is_paid,
            'is_cancelled': instance.is_cancelled,
        }

        progress_percentage = 0

        # Make a progress-percentage based on the 5-types of order-status
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


        # Send this "data-dict" to the 'order_status' channel of the 'OrderProgress' consumer.
        channel_layer = get_channel_layer() # fetch all the channel layers

        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,
            {
                'type': 'order_status', # will call the 'order_status' method from the "OrderProgress" consumer which is in the "foodsystem\cartOrder\consumers.py" file.
                'value': json.dumps(data),  # converts the python-dict into json-string-object
            }
        )

