"""
ASGI config for foodsystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
import cartOrder.routing

# It's a default code-line, sice the project gets initialized
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodsystem.settings')

# application = get_asgi_application()


application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Optional; http-> django views is added by default
    "websocket": AuthMiddlewareStack(
        URLRouter(
            cartOrder.routing.websocket_urlpatterns
        )
    ),
})
