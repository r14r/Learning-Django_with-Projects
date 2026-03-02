from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester', password='secret123'
        )

    def test_register_view(self):
        resp = self.client.get(reverse('user_auth:register'))
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse('user_auth:list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_profile_created_on_register(self):
        self.client.post(reverse('user_auth:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(user, 'profile'))

    def test_profile_edit(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(reverse('user_auth:update'), {
            'bio': 'Hello world',
            'location': 'NYC',
            'website': '',
        })
        self.assertEqual(resp.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Hello world')

    def test_profile_view(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.get(
            reverse('user_auth:detail', kwargs={'pk': self.user.profile.pk})
        )
        self.assertEqual(resp.status_code, 200)
