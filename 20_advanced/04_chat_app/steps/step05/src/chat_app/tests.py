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

    def test_room_view(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.get(reverse('chat_app:room', kwargs={'slug': 'general'}))
        self.assertEqual(resp.status_code, 200)

    def test_create_room(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('chat_app:create'), {'name': 'Tech', 'slug': 'tech'})
        self.assertEqual(Room.objects.count(), 2)

    def test_message_stored(self):
        Message.objects.create(room=self.room, author=self.user, content='Hello!')
        self.assertEqual(Message.objects.count(), 1)
