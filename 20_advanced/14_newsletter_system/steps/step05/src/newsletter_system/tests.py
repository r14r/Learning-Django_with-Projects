from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from .models import Subscriber, Campaign


class NewsletterTests(TestCase):
    def setUp(self):
        self.client_http = Client()
        self.user        = User.objects.create_user('admin', password='pass')
        self.sub         = Subscriber.objects.create(email='alice@example.com', confirmed=True)

    def test_subscribe(self):
        resp = self.client_http.post(reverse('newsletter_system:subscribe'), {
            'email': 'new@example.com', 'name': 'Bob'
        })
        self.assertEqual(Subscriber.objects.filter(email='new@example.com').count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_confirm_subscription(self):
        sub = Subscriber.objects.create(email='confirm@example.com')
        resp = self.client_http.get(
            reverse('newsletter_system:confirm', kwargs={'token': sub.token})
        )
        sub.refresh_from_db()
        self.assertTrue(sub.confirmed)

    def test_unsubscribe(self):
        resp = self.client_http.get(
            reverse('newsletter_system:unsubscribe', kwargs={'token': self.sub.token})
        )
        self.sub.refresh_from_db()
        self.assertFalse(self.sub.confirmed)

    def test_send_campaign(self):
        self.client_http.login(username='admin', password='pass')
        campaign = Campaign.objects.create(
            owner=self.user, subject='Test Campaign', body_text='Hello!'
        )
        self.client_http.post(
            reverse('newsletter_system:send', kwargs={'pk': campaign.pk})
        )
        campaign.refresh_from_db()
        self.assertIsNotNone(campaign.sent_at)
        self.assertEqual(len(mail.outbox), 1)  # 1 confirmed subscriber
