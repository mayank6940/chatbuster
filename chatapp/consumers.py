

import firebase_admin
from firebase_admin import db
from django.conf import settings
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime

firebase_admin.initialize_app()

class ChatConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_id = self.scope['url_route']['kwargs']['room_id']
        sender_username = self.scope['user'].username

        
        ref = db.reference(f'/chat_rooms/{room_id}/messages')
        ref.push({
            'sender': sender_username,
            'message': message,
            'timestamp': datetime.now().isoformat(),
        })

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
