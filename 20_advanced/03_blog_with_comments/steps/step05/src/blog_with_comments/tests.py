from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Post, Tag, Comment


class PostTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user   = User.objects.create_user('alice', password='pass')
        self.tag    = Tag.objects.create(name='Django', slug='django')
        self.post   = Post.objects.create(
            title='Hello World', slug='hello-world', author=self.user,
            body='Test post body', status='published', publish=timezone.now(),
        )
        self.post.tags.add(self.tag)

    def test_list_view(self):
        resp = self.client.get(reverse('blog_with_comments:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello World')

    def test_draft_hidden(self):
        Post.objects.create(
            title='Draft Post', slug='draft-post', author=self.user,
            body='hidden', status='draft', publish=timezone.now(),
        )
        resp = self.client.get(reverse('blog_with_comments:list'))
        self.assertNotContains(resp, 'Draft Post')

    def test_detail_view(self):
        p = self.post.publish
        resp = self.client.get(
            reverse('blog_with_comments:detail',
                    kwargs={'year': p.year, 'month': p.month, 'day': p.day, 'slug': self.post.slug})
        )
        self.assertEqual(resp.status_code, 200)

    def test_tag_filter(self):
        resp = self.client.get(
            reverse('blog_with_comments:tag', kwargs={'slug': 'django'})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello World')

    def test_comment_requires_login(self):
        p = self.post.publish
        url = reverse('blog_with_comments:add-comment', kwargs={'pk': self.post.pk})
        resp = self.client.post(url, {'body': 'Great post!'})
        self.assertNotEqual(resp.status_code, 200)

    def test_add_comment(self):
        self.client.login(username='alice', password='pass')
        url = reverse('blog_with_comments:add-comment', kwargs={'pk': self.post.pk})
        self.client.post(url, {'body': 'Great post!'})
        self.assertEqual(Comment.objects.count(), 1)
