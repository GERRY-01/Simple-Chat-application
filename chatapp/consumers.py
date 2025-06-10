import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from  .models import Message,Room
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    
    def get_room_name(self, user1_id, user2_id):
            ids = sorted([user1_id, user2_id])
            return f'chat_{ids[0]}_{ids[1]}'
        
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = int(self.scope["url_route"]["kwargs"]["other_user_id"])
        self.room_name = self.get_room_name(self.user.id, self.other_user_id)
        self.room_group_name = f'chat_{self.room_name}'
        self.room,_ = await database_sync_to_async(Room.objects.get_or_create)(name=self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.user
        receiver = await database_sync_to_async(User.objects.get)(id=self.other_user_id)

        # Save message to database
        await database_sync_to_async(Message.objects.create)(
            room=self.room,
            sender=sender,
            receiver=receiver,
            message=message
        )
        
        #broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.id,
                'receiver': receiver.id
            }
        )
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver
        }))

