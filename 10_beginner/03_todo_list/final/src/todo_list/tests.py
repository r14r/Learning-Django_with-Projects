from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Todo


class TodoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.todo = Todo.objects.create(
            title='Buy groceries', priority='high', author=self.user
        )

    def test_list_requires_login(self):
        resp = self.client.get(reverse('todo_list:list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_list_view(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.get(reverse('todo_list:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Buy groceries')

    def test_create_todo(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(
            reverse('todo_list:create'),
            {'title': 'New Task', 'priority': 'medium'}
        )
        self.assertEqual(Todo.objects.count(), 2)

    def test_toggle_done(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(reverse('todo_list:toggle', kwargs={'pk': self.todo.pk}))
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_done)

    def test_delete_todo(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(reverse('todo_list:delete', kwargs={'pk': self.todo.pk}))
        self.assertEqual(Todo.objects.count(), 0)
