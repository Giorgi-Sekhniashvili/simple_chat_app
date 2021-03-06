from typing import Optional, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Q

UserModel: AbstractBaseUser = get_user_model()


class PrivateChat(models.Model):
    encoded_chat_name = models.CharField(max_length=64, unique=True)

    user1 = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='user2')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user1', 'user2'), ('user2', 'user1')]
        verbose_name = 'Private chat'
        verbose_name_plural = 'Private chat rooms'

    def __str__(self):
        return f'chat with: {self.user1}, {self.user2}'

    @staticmethod
    def chat_room_exists(user1: AbstractBaseUser, user2: AbstractBaseUser) -> Optional[Any]:
        return PrivateChat.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).first()

    @staticmethod
    def create_if_not_exists(user1: AbstractBaseUser, user2: AbstractBaseUser):
        res = PrivateChat.chat_room_exists(user1, user2)
        if not res:
            private_chat = PrivateChat.objects.create(user1=user1, user2=user2)
            return private_chat

    @staticmethod
    def get_chat_rooms_for_user(user: AbstractBaseUser):
        return PrivateChat.objects.filter(Q(user1=user) | Q(user2=user))


class PrivateChatMessage(models.Model):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    chat = models.ForeignKey(to=PrivateChat, on_delete=models.CASCADE)

    content = models.TextField(blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Private chat message'
        verbose_name_plural = 'Private chat messages'

    def __str__(self):
        return f'chat_id: {self.chat_id}, user_id: {self.user_id}'
