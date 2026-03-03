from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Quiz, Question, Choice, QuizResult


class QuizAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.quiz = Quiz.objects.create(
            title='Test Quiz', description='A test', author=self.user
        )
        self.q1 = Question.objects.create(quiz=self.quiz, text='What is 2+2?', order=1)
        self.correct = Choice.objects.create(question=self.q1, text='4', is_correct=True)
        Choice.objects.create(question=self.q1, text='3', is_correct=False)

    def test_list_view(self):
        resp = self.client.get(reverse('quiz_app:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Quiz')

    def test_detail_view(self):
        resp = self.client.get(reverse('quiz_app:detail', kwargs={'pk': self.quiz.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_take_quiz_requires_login(self):
        resp = self.client.get(reverse('quiz_app:take', kwargs={'pk': self.quiz.pk}))
        self.assertNotEqual(resp.status_code, 200)

    def test_take_quiz_scoring(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('quiz_app:take', kwargs={'pk': self.quiz.pk}),
            {f'question_{self.q1.pk}': str(self.correct.pk)},
        )
        self.assertEqual(resp.status_code, 302)
        result = QuizResult.objects.first()
        self.assertEqual(result.score, 1)
        self.assertEqual(result.total, 1)

    def test_quiz_create(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(reverse('quiz_app:create'), {
            'title': 'New Quiz',
            'description': 'A new quiz',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Quiz.objects.count(), 2)
