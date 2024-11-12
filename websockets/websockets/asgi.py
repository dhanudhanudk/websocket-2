# your_project_name/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatapp import routing  # Import the routing for chat

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websockets.settings')  # Replace with your project's name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

ASGI_APPLICATION = 'websockets.asgi.application'