from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ContactMessage


class ContactFormTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(username='admin', password='pass123')

    def test_public_form_get(self):
        resp = self.client.get(reverse('contact_form:list'))
        self.assertEqual(resp.status_code, 200)

    def test_submit_contact(self):
        resp = self.client.post(reverse('contact_form:list'), {
            'name': 'Alice',
            'email': 'alice@example.com',
            'subject': 'Hello',
            'message': 'Test message',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_inbox_requires_login(self):
        resp = self.client.get(reverse('contact_form:inbox'))
        self.assertNotEqual(resp.status_code, 200)

    def test_mark_read(self):
        msg = ContactMessage.objects.create(
            name='Bob', email='bob@example.com',
            subject='Hi', message='Hello',
        )
        self.client.login(username='admin', password='pass123')
        self.client.post(reverse('contact_form:mark-read', kwargs={'pk': msg.pk}))
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)

    def test_message_str(self):
        msg = ContactMessage(name='Carol', subject='Test')
        self.assertIn('Carol', str(msg))
