from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Choice, Poll


class PollTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.poll = Poll.objects.create(
            question='Favorite language?',
            author=self.user,
        )
        self.choice1 = Choice.objects.create(poll=self.poll, text='Python')
        self.choice2 = Choice.objects.create(poll=self.poll, text='JavaScript')

    def test_list_view(self):
        resp = self.client.get(reverse('poll_app:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Favorite language?')

    def test_detail_view(self):
        resp = self.client.get(reverse('poll_app:detail', kwargs={'pk': self.poll.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Python')

    def test_vote(self):
        self.client.post(
            reverse('poll_app:vote', kwargs={'pk': self.poll.pk}),
            {'choice': self.choice1.pk},
        )
        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('poll_app:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_multiple_choices(self):
        self.assertEqual(self.poll.choices.count(), 2)
        Choice.objects.create(poll=self.poll, text='Go')
        self.assertEqual(self.poll.choices.count(), 3)
