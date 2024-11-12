from datetime import datetime, timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import*

class Consumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()  # Accept the WebSocket connection
        print("Server connected")

    async def receive(self, text_data):
        data = json.loads(text_data)

        room_name = data.get('room')  # This should correspond to a string identifier
        sender = data.get('sender')
        receiver = data.get('receiver')
        message = data.get('message')

        # Get sender's name
        sender_name = await self.get_sender_name(sender)

        # Ensure the room exists or create it
        room, created = await database_sync_to_async(ChatRoom.objects.get_or_create)(room_name=room_name)

        # Create a message box entry
        message_box = MassageBox(room_id=room.id, sender_id=sender, receiver_id=receiver, message=message)
        await database_sync_to_async(message_box.save)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatmessage',
                'sender': sender_name,
                'receiver': receiver,
                'message': message,
                'room_id': room.id,
            },
        )

    # Receive message from room group
    async def chatmessage(self, event):
        sender = event['sender']
        receiver = event['receiver']
        message = event['message']
        room_id = event['room_id']

        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'room_id': room_id
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,  # This should match your group name
            self.channel_name
        )

    async def get_sender_name(self, sender_id):
        user = await database_sync_to_async(User.objects.get)(id=sender_id)
        return user.name  # Assuming you want the username, change to user.name if that’s the field you need
