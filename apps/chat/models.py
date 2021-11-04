from typing import Optional, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import Q

UserModel: AbstractBaseUser = get_user_model()


class PrivateChat(models.Model):
    user1 = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    user2 = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))
        verbose_name = 'Private chat'
        verbose_name_plural = 'Private chat rooms'

    def __str__(self):
        return f'chat with: {self.user1_id}, {self.user2_id}'

    @staticmethod
    def chat_room_exists(user1: AbstractBaseUser, user2: AbstractBaseUser) -> Optional[Any]:
        return PrivateChat.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).first()

    @staticmethod
    def create_if_not_exists(user1: AbstractBaseUser, user2: AbstractBaseUser):
        res = PrivateChat.chat_room_exists(user1, user2)
        if not res:
            PrivateChat.objects.create(user1=user1, user2=user2)

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
        ordering = ['-time_created']
        verbose_name = 'Private chat message'
        verbose_name_plural = 'Private chat messages'

    def __str__(self):
        return f'chat_id: {self.chat_id}, user_id: {self.user_id}'
