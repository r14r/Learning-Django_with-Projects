from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Item

class ItemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester', password='secret123'
        )
        self.item = Item.objects.create(
            title='Test Item',
            description='A test item',
            author=self.user,
        )

    def test_list_view(self):
        resp = self.client.get(reverse('testing_framework:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Item')

    def test_detail_view(self):
        resp = self.client.get(
            reverse('testing_framework:detail', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('testing_framework:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_item(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('testing_framework:create'),
            {'title': 'New Item', 'description': 'Created in test'},
        )
        self.assertEqual(Item.objects.count(), 2)

    def test_delete_item(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('testing_framework:delete', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(Item.objects.count(), 0)