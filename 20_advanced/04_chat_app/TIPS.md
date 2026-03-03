# Tips & Implementation Guide: Real-Time Chat

## 1. Install Channels

```bash
pip install django channels channels-redis daphne
```

## 2. settings.py

```python
INSTALLED_APPS = [
    ...
    'daphne',
    'channels',
    'chat_app',
]
ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]},
    }
}
```

For development without Redis, use the in-memory layer:
```python
CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
```

## 3. ASGI config

```python
# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http':      get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(chat_app.routing.websocket_urlpatterns)),
})
```

## 4. WebSocket Consumer

```python
# chat_app/consumers.py
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
        message = data['message']
        user    = self.scope['user']
        await self.save_message(user, message)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat_message',
            'message': message,
            'username': user.username,
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message':  event['message'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, user, content):
        from .models import Room, Message
        room = Room.objects.get(slug=self.room_slug)
        Message.objects.create(room=room, author=user, content=content)
```

## 5. Routing

```python
# chat_app/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<slug>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
```

## 6. Front-end JavaScript snippet

```javascript
const ws = new WebSocket(`ws://${window.location.host}/ws/chat/${roomSlug}/`);
ws.onmessage = (e) => {
    const data = JSON.parse(e.data);
    chatBox.innerHTML += `<p><strong>${data.username}:</strong> ${data.message}</p>`;
};
document.querySelector('#send-btn').onclick = () => {
    ws.send(JSON.stringify({message: document.querySelector('#msg-input').value}));
};
```
