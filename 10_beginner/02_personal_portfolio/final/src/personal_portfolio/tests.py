from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project


class ProjectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.project = Project.objects.create(
            title='My First App', description='A test project',
            technology='Python/Django', author=self.user
        )

    def test_list_view(self):
        resp = self.client.get(reverse('personal_portfolio:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'My First App')

    def test_detail_view(self):
        resp = self.client.get(reverse('personal_portfolio:detail', kwargs={'pk': self.project.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('personal_portfolio:create'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_project(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('personal_portfolio:create'),
            {'title': 'New Project', 'description': 'Desc', 'technology': 'Python'}
        )
        self.assertEqual(Project.objects.count(), 2)

    def test_delete_project(self):
        self.client.login(username='tester', password='secret123')
        self.client.post(reverse('personal_portfolio:delete', kwargs={'pk': self.project.pk}))
        self.assertEqual(Project.objects.count(), 0)
