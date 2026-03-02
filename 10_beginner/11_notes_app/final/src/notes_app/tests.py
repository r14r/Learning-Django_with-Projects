from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Note


class NoteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.other = User.objects.create_user(username='other', password='secret123')
        self.note = Note.objects.create(
            title='Test Note',
            content='Some content',
            author=self.user,
        )

    def test_list_requires_login(self):
        resp = self.client.get(reverse('notes_app:list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_list_shows_own_notes(self):
        Note.objects.create(title='Other Note', content='x', author=self.other)
        self.client.login(username='tester', password='secret123')
        resp = self.client.get(reverse('notes_app:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Note')
        self.assertNotContains(resp, 'Other Note')

    def test_create_note(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('notes_app:create'),
            {'title': 'New Note', 'content': 'Body', 'color': '#ffffff', 'pinned': False},
        )
        self.assertEqual(Note.objects.count(), 2)

    def test_toggle_pin(self):
        self.client.login(username='tester', password='secret123')
        self.assertFalse(self.note.pinned)
        self.client.post(reverse('notes_app:pin', kwargs={'pk': self.note.pk}))
        self.note.refresh_from_db()
        self.assertTrue(self.note.pinned)

    def test_delete_note(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(reverse('notes_app:delete', kwargs={'pk': self.note.pk}))
        self.assertEqual(Note.objects.count(), 0)
