from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import ShortURL


class ShortURLTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.short = ShortURL.objects.create(
            original_url='https://www.example.com',
            short_code='abc123',
            created_by=self.user,
        )

    def test_shorten_view_get(self):
        resp = self.client.get(reverse('url_shortener:list'))
        self.assertEqual(resp.status_code, 200)

    def test_shorten_url(self):
        resp = self.client.post(
            reverse('url_shortener:list'),
            {'original_url': 'https://www.djangoproject.com'},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ShortURL.objects.count(), 2)

    def test_redirect_increments_clicks(self):
        resp = self.client.get(reverse('url_shortener:redirect', kwargs={'short_code': 'abc123'}))
        self.assertEqual(resp.status_code, 302)
        self.short.refresh_from_db()
        self.assertEqual(self.short.clicks, 1)

    def test_my_urls_requires_login(self):
        resp = self.client.get(reverse('url_shortener:my-urls'))
        self.assertNotEqual(resp.status_code, 200)

    def test_delete_url(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(reverse('url_shortener:delete', kwargs={'pk': self.short.pk}))
        self.assertEqual(ShortURL.objects.count(), 0)
