from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task, Label


class TaskTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user   = User.objects.create_user('alice', password='pass')
        self.task   = Task.objects.create(
            title='Fix bug', priority='high', owner=self.user
        )

    def test_list_requires_login(self):
        resp = self.client.get(reverse('task_manager:list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_list_view(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.get(reverse('task_manager:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Fix bug')

    def test_create_task(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('task_manager:create'), {
            'title': 'New Task', 'priority': 'medium', 'status': 'todo',
        })
        self.assertEqual(Task.objects.count(), 2)

    def test_update_status(self):
        self.client.login(username='alice', password='pass')
        self.client.post(
            reverse('task_manager:update-status',
                    kwargs={'pk': self.task.pk, 'status': 'done'})
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'done')

    def test_delete_task(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('task_manager:delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(Task.objects.count(), 0)

    def test_overdue_flag(self):
        from datetime import date
        self.task.due_date = date(2000, 1, 1)
        self.task.save()
        self.assertTrue(self.task.is_overdue)

    def test_board_view(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.get(reverse('task_manager:board'))
        self.assertEqual(resp.status_code, 200)
