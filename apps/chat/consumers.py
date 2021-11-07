import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import PrivateChat, PrivateChatMessage
from .serializers import PrivateChatMessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    chat_room = None
    chat_room_channel = None

    async def connect(self):
        if self.scope['user'].is_authenticated:
            encoded_chat_name = self.scope['url_route']['kwargs'].get('chat_name')

            self.chat_room = await self.get_private_chat(encoded_chat_name=encoded_chat_name)
            self.chat_room_channel = f'chat_room_{self.chat_room.id}'
            users_in_chat = await self.get_users_from_chat()

            if self.scope['user'] in users_in_chat:
                await self.channel_layer.group_add(self.chat_room_channel, self.channel_name)
                await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_room_channel, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        chat_message = await self.create_chat_message(user=self.scope['user'], chat=self.chat_room, content=text_data_json.get('newMessage'))
        chat_message_serializer = PrivateChatMessageSerializer(chat_message)

        await self.channel_layer.group_send(
            self.chat_room_channel,
            {
                'type': 'private.chat.message',
                'message': chat_message_serializer.data
            }
        )

    @database_sync_to_async
    def get_private_chat(self, encoded_chat_name):
        private_chat = PrivateChat.objects.get(encoded_chat_name=encoded_chat_name)
        return private_chat

    @database_sync_to_async
    def create_chat_message(self, user, chat, content):
        chat_message = PrivateChatMessage(user=user, chat=chat, content=content)
        chat_message.save()
        return chat_message

    @sync_to_async
    def get_users_from_chat(self):
        return [self.chat_room.user1, self.chat_room.user2]

    async def private_chat_message(self, event):
        new_message = event['message']
        await self.send(text_data=json.dumps(new_message))
