from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Item


class ItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', password='secret123'
        )
        self.item = Item.objects.create(
            title='Test Item',
            description='A test item',
            author=self.user,
        )

    def test_item_str(self):
        self.assertEqual(str(self.item), 'Test Item')

    def test_item_ordering(self):
        Item.objects.create(title='Older', description='', author=self.user)
        items = list(Item.objects.values_list('title', flat=True))
        self.assertEqual(items[0], 'Older')  # most recent first

    def test_item_has_timestamps(self):
        self.assertIsNotNone(self.item.created_at)
        self.assertIsNotNone(self.item.updated_at)


class ItemViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester', password='secret123'
        )
        self.other = User.objects.create_user(
            username='other', password='secret123'
        )
        self.item = Item.objects.create(
            title='Test Item',
            description='A test item',
            author=self.user,
        )

    def test_list_view(self):
        resp = self.client.get(reverse('docker_deployment:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Item')

    def test_detail_view(self):
        resp = self.client.get(
            reverse('docker_deployment:detail', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Item')

    def test_create_requires_login(self):
        resp = self.client.get(reverse('docker_deployment:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_item(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('docker_deployment:create'),
            {'title': 'New Item', 'description': 'Created in test'},
        )
        self.assertEqual(Item.objects.count(), 2)

    def test_delete_item(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('docker_deployment:delete', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(Item.objects.count(), 0)

    def test_update_requires_login(self):
        resp = self.client.get(
            reverse('docker_deployment:update', kwargs={'pk': self.item.pk})
        )
        self.assertNotEqual(resp.status_code, 200)

    def test_update_item(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('docker_deployment:update', kwargs={'pk': self.item.pk}),
            {'title': 'Updated Title', 'description': 'Updated description'},
        )
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, 'Updated Title')

    def test_create_sets_author(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('docker_deployment:create'),
            {'title': 'Author Item', 'description': 'test'},
        )
        new_item = Item.objects.get(title='Author Item')
        self.assertEqual(new_item.author, self.user)

    def test_list_view_empty(self):
        Item.objects.all().delete()
        resp = self.client.get(reverse('docker_deployment:list'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view_404(self):
        resp = self.client.get(
            reverse('docker_deployment:detail', kwargs={'pk': 9999})
        )
        self.assertEqual(resp.status_code, 404)

    def test_create_invalid_form(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('docker_deployment:create'),
            {'title': '', 'description': 'no title'},
        )
        self.assertEqual(Item.objects.count(), 1)

    def test_delete_requires_login(self):
        resp = self.client.get(
            reverse('docker_deployment:delete', kwargs={'pk': self.item.pk})
        )
        self.assertNotEqual(resp.status_code, 200)

    def test_multiple_users_items_in_list(self):
        Item.objects.create(
            title='Other User Item', description='', author=self.other
        )
        resp = self.client.get(reverse('docker_deployment:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Other User Item')
        self.assertContains(resp, 'Test Item')
