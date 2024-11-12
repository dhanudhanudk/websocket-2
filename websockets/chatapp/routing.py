# chat/routing.py
from django.urls import path
from . import consumers  # Ensure this imports your WebSocket consumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.Consumers.as_asgi()),
]