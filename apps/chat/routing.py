from .consumers import ChatConsumer
from django.urls import path


websocket_urlpatterns = [
    path('ws/chat/<str:chat_name>/', ChatConsumer.as_asgi()),
]
