import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import PrivateChat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            user1 = self.scope['user']
            # TODO get second user
            user2 = None
            # TODO get chat room
            self.chat_room = await self.get_private_chat(user1=user1, user2=user2)
            self.chat_room_channel = f'chat_room_{self.chat_room.id}'

            await self.channel_layer.group_add(self.chat_room_channel, self.channel_name)
            await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_room_channel, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        await self.channel_layer.group_send(
            self.chat_room_channel,
            {
                'type': 'private.chat.message',
                'message': message
            }
        )

    @database_sync_to_async
    def get_private_chat(self, user1, user2):
        private_chat = PrivateChat.create_if_not_exists(user1, user2)
        return private_chat

    async def private_chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))
