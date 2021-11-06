import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import PrivateChat, PrivateChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            encoded_chat_name = self.scope['url_route']['kwargs'].get('chat_name')
            self.chat_room = await self.get_private_chat(encoded_chat_name=encoded_chat_name)
            self.chat_room_channel = f'chat_room_{self.chat_room.id}'

            await self.channel_layer.group_add(self.chat_room_channel, self.channel_name)
            await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_room_channel, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        await self.channel_layer.group_send(
            self.chat_room_channel,
            {
                'type': 'private.chat.message',
                'message': 'hi'
            }
        )

    @database_sync_to_async
    def get_private_chat(self, encoded_chat_name):
        private_chat = PrivateChat.objects.get(encoded_chat_name=encoded_chat_name)
        return private_chat

    @database_sync_to_async
    def create_chat_message(self, content):
        chat_message = PrivateChatMessage(user=self.scope['user'], chat=self.chat_room, content=content)
        chat_message.save()
        return chat_message

    async def private_chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))
