# Step 5 – Tests & Deployment

## chat_app/tests.py

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Room, Message

class ChatTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user   = User.objects.create_user('alice', password='pass')
        self.room   = Room.objects.create(name='General', slug='general')

    def test_room_list_requires_login(self):
        resp = self.client.get(reverse('chat_app:list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_room_list(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.get(reverse('chat_app:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'General')
```
