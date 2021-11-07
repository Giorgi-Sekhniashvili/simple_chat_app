from hashlib import sha256

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PrivateChat
from .serializers import PrivateChatMessageSerializer

UserModel: AbstractBaseUser = get_user_model()


class IndexPageView(View):
    template_name = 'chat/index.html'

    def get(self, request):
        user = self.request.user
        if user.is_authenticated:
            context = {
                'users': UserModel.objects.filter(~Q(id=user.id)),
                'chats': PrivateChat.objects.filter(Q(user1=user) | Q(user2=user))
            }
        else:
            context = {}

        return render(request, self.template_name, context=context)

    def post(self, request):
        user1_id = int(request.POST.get('user1_id'))
        if request.user.id != user1_id:
            return HttpResponseForbidden()
        user2_id = int(request.POST.get('user2_id'))

        user1 = UserModel.objects.get(id=user1_id)
        user2 = UserModel.objects.get(id=user2_id)
        encoded_chat_name1 = sha256(f'{user1.get_username()}{user2.get_username()}'.encode('utf-8')).hexdigest()
        encoded_chat_name2 = sha256(f'{user2.get_username()}{user1.get_username()}'.encode('utf-8')).hexdigest()
        try:
            private_chat = PrivateChat.objects.get(encoded_chat_name=encoded_chat_name1)
        except PrivateChat.DoesNotExist:
            try:
                private_chat = PrivateChat.objects.get(encoded_chat_name=encoded_chat_name2)
            except PrivateChat.DoesNotExist:
                private_chat = PrivateChat(encoded_chat_name=encoded_chat_name1, user1=user1, user2=user2)
                private_chat.save()

        return redirect(to='chat:chat', chat_name=private_chat.encoded_chat_name)


class PrivateChatView(View):
    def get(self, request, chat_name):
        private_chat = PrivateChat.objects.get(encoded_chat_name=chat_name)
        print(private_chat)
        context = {
            'private_chat': private_chat,
            'messages': private_chat.privatechatmessage_set.all()
        }
        return render(request, 'chat/private_chat.html', context=context)


class ChatMessagesAPIView(APIView):
    def get(self, request, chat_name):
        print(chat_name)
        chat_room = PrivateChat.objects.get(encoded_chat_name=chat_name)
        messages = chat_room.privatechatmessage_set.all()

        message_serializer = PrivateChatMessageSerializer(messages, many=True)
        return Response(data=message_serializer.data)
