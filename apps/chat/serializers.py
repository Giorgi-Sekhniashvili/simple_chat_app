from rest_framework import serializers

from .models import PrivateChatMessage


class PrivateChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChatMessage
        fields = ['id', 'user', 'chat', 'content', 'created']
        read_only_fields = ['id', 'user', 'created']
