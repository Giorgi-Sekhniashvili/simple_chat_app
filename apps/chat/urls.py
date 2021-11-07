from django.urls import path

from .views import IndexPageView, PrivateChatView, ChatMessagesAPIView

app_name = 'chat'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('chat/<str:chat_name>/', PrivateChatView.as_view(), name='chat'),
    path('api/chat/<str:chat_name>/', ChatMessagesAPIView.as_view(), name='chat_messages')
]
