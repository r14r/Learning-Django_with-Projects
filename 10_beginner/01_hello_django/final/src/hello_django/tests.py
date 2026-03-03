from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Message


class MessageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.msg = Message.objects.create(
            title='Hello World', body='First message.', author=self.user
        )

    def test_list_view(self):
        resp = self.client.get(reverse('hello_django:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello World')

    def test_detail_view(self):
        resp = self.client.get(reverse('hello_django:detail', kwargs={'pk': self.msg.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('hello_django:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_message(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('hello_django:create'),
            {'title': 'New Msg', 'body': 'Body text'}
        )
        self.assertEqual(Message.objects.count(), 2)

    def test_delete_message(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(reverse('hello_django:delete', kwargs={'pk': self.msg.pk}))
        self.assertEqual(Message.objects.count(), 0)
