from .consumers import ChatConsumer
from django.urls import path


websocket_urlpatterns = [
    path('ws/chat/<str:user2_id>/', ChatConsumer.as_asgi()),
]
