from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, Post, Comment


class SocialNetworkTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.alice  = User.objects.create_user('alice', password='pass')
        self.bob    = User.objects.create_user('bob', password='pass')
        self.post   = Post.objects.create(author=self.alice, body='Hello World!')

    def test_profile_auto_created(self):
        self.assertTrue(hasattr(self.alice, 'profile'))

    def test_feed_requires_login(self):
        resp = self.client.get(reverse('social_network:feed'))
        self.assertNotEqual(resp.status_code, 200)

    def test_explore_page(self):
        resp = self.client.get(reverse('social_network:explore'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello World!')

    def test_profile_page(self):
        resp = self.client.get(
            reverse('social_network:profile', kwargs={'username': 'alice'})
        )
        self.assertEqual(resp.status_code, 200)

    def test_follow_unfollow(self):
        self.client.login(username='bob', password='pass')
        self.client.post(
            reverse('social_network:follow', kwargs={'username': 'alice'})
        )
        self.assertIn(self.alice, self.bob.profile.following.all())
        self.client.post(
            reverse('social_network:follow', kwargs={'username': 'alice'})
        )
        self.assertNotIn(self.alice, self.bob.profile.following.all())

    def test_like_post(self):
        self.client.login(username='bob', password='pass')
        self.client.post(
            reverse('social_network:like', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(self.post.like_count, 1)

    def test_feed_shows_followed_posts(self):
        self.client.login(username='bob', password='pass')
        self.bob.profile.following.add(self.alice)
        resp = self.client.get(reverse('social_network:feed'))
        self.assertContains(resp, 'Hello World!')
