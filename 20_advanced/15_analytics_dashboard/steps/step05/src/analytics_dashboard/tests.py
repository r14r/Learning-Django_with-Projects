from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import PageView, Event


class AnalyticsTests(TestCase):
    def setUp(self):
        self.client_http = Client()
        self.user        = User.objects.create_user('admin', password='pass')
        # Create sample page views
        for i in range(5):
            PageView.objects.create(path='/page/', timestamp=timezone.now())
        PageView.objects.create(path='/other/', timestamp=timezone.now())

    def test_dashboard_requires_login(self):
        resp = self.client_http.get(reverse('analytics_dashboard:dashboard'))
        self.assertNotEqual(resp.status_code, 200)

    def test_dashboard_view(self):
        self.client_http.login(username='admin', password='pass')
        resp = self.client_http.get(reverse('analytics_dashboard:dashboard'))
        self.assertEqual(resp.status_code, 200)

    def test_record_event_api(self):
        resp = self.client_http.post(
            reverse('analytics_dashboard:event'),
            {'name': 'button_click', 'properties': '{}'},
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Event.objects.count(), 1)

    def test_top_pages(self):
        from django.db.models import Count
        top = PageView.objects.values('path').annotate(count=Count('id')).order_by('-count')
        self.assertEqual(top[0]['path'], '/page/')
        self.assertEqual(top[0]['count'], 5)
