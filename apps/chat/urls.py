from django.urls import path

from .views import IndexPageView, PrivateChatView

app_name = 'chat'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('chat/<int:user2_id>/', PrivateChatView.as_view(), name='chat')
]
