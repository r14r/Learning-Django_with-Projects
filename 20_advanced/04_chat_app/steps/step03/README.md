# Step 3 – WebSocket Consumer

## chat_app/consumers.py

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug  = self.scope['url_route']['kwargs']['slug']
        self.group_name = f'chat_{self.room_slug}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data    = json.loads(text_data)
        content = data['message']
        user    = self.scope['user']
        await self.save_message(user, content)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat_message', 'message': content, 'username': user.username,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'], 'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, user, content):
        from .models import Room, Message
        room = Room.objects.get(slug=self.room_slug)
        Message.objects.create(room=room, author=user, content=content)
```
