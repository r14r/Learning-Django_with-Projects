from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post


class PostTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.post = Post.objects.create(
            title='Test Post', body='Post body content.', author=self.user
        )

    def test_list_view(self):
        resp = self.client.get(reverse('simple_blog:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Post')

    def test_detail_view(self):
        resp = self.client.get(reverse('simple_blog:detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('simple_blog:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_post(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('simple_blog:create'),
            {'title': 'New Post', 'body': 'Content here'}
        )
        self.assertEqual(Post.objects.count(), 2)

    def test_slug_auto_generated(self):
        self.assertEqual(self.post.slug, 'test-post')

    def test_delete_post(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(reverse('simple_blog:delete', kwargs={'slug': self.post.slug}))
        self.assertEqual(Post.objects.count(), 0)
