from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from asgiref.sync import async_to_sync, sync_to_async



class OrderProgress(WebsocketConsumer):
    def connect(self):
        # create a room for a specific order using its order_id, this ['order_id'] is fetched from the websocket's 'routing.py' file's route-path.
        # This websocket routing-path will be hit by the frontend-websockets instance.
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        print('Room Name: ', self.room_name)
        self.room_group_name = 'order_%s' % self.room_name  # the 'ws/food-order/<order_id>/' pattern from the 'routing.py' file
        print('Backend Consumer (Websocket): Connected')

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name   # why do we need to use "channel_name" instead of "room_name"; (channel automatically fixes for us?)
        )

        async_to_sync(self.accept())

        # Fetch the current info of this specific-order using the 'mode.py' file's staticmethod ("get_order_detail")
        # 'self.room_name' collects the order-id.
        # 'self.room_name' equals to the order-id, which is sent as the pararm inside the "get_order_detail" staticmethod. This staticmethod exists inside the "pizzaProj/home/models.py" file.
        # Whenever the sockets get connected, it'll make a query to fetch the order-data using the staticmethod ("get_order_detail") & json-dumps into the room_group.
        # So everytime, when the page is reloaded, the frontend-websocket makes a connection with this consumer ("OrderProgress"), so the consumer's 'connect' method normally calls the staticmethod ("get_order_detail") to make query of that specific order-id, extract the data-payload & dumps to that individual-channel-room.
        order = Order.get_order_detail(self.room_name)

        # Whenever this frontend-websocket connects with this consumer, immedietly send a json-response-data to the frontend-websocket.
        # This is initially displayed in the 'websocketking.com' if its channel-route is connected.
        self.send(text_data=json.dumps({
            'status': 'Backend Consumer (Websocket): Connected - hit from frontend',
            'payload': order,
        }))
    
    # Extract the payload from the 'order_status' channel-method & send that to the channel-room-group, so that every frontend-websocket can receive the payload in the frontend.
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status', # will call the 'order_status' method from below
                'payload': text_data,
            }
        )
        # return super().receive(text_data=text_data, bytes_data=bytes_data)


    # Single channel-method; the data which is received by this channel will be extracted/ fetched by the receiver-channel of this consumer, which then will be sent to the channel-group.
    # The payloads will be sent from a post-save-signal of the 'models.py' file.
    # Working as a receiver to receive the payloads store in the single channel, which will then be extract by the channel-group-receiver and send to the room-group. So that every frontend-websocket can receive the payload.
    # This channel method is called in the 'models.py' file to send the order-post-insert-query in this channel.
    def order_status(self, event):
        print('*' * 50)
        print('Custome Consumer/ Websocket: %s' % event)
        print('*' * 50)
        order = json.loads(event.get('value'))
        self.send(text_data=json.dumps({
            'payload': order
        }))


    def disconnect(self, *args, **kwargs):
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('Backend Consumer (Websocket): Disconnected!')    
        pass