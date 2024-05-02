from django.urls import re_path, path
from . import consumers


websocket_urlpatterns = [
    path('ws/food-order/<order_id>/', consumers.OrderProgress.as_asgi()),
]