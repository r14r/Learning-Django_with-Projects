from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Course, Grade


class GradeTrackerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.course = Course.objects.create(
            name='Mathematics',
            code='MATH101',
            student=self.user,
        )
        self.grade = Grade.objects.create(
            course=self.course,
            assignment='Midterm',
            score=85,
            max_score=100,
        )

    def test_list_requires_login(self):
        resp = self.client.get(reverse('grade_tracker:list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_course_list_view(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.get(reverse('grade_tracker:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mathematics')

    def test_create_course(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('grade_tracker:create'),
            {'name': 'Physics', 'code': 'PHY101', 'description': ''},
        )
        self.assertEqual(Course.objects.count(), 2)

    def test_add_grade(self):
        self.client.login(username='tester', password='secret123')
        resp = self.client.post(
            reverse('grade_tracker:grade-add', kwargs={'course_pk': self.course.pk}),
            {'assignment': 'Final Exam', 'score': '92', 'max_score': '100'},
        )
        self.assertEqual(self.course.grades.count(), 2)

    def test_average_grade_property(self):
        Grade.objects.create(course=self.course, assignment='Final', score=95, max_score=100)
        avg = self.course.average_grade
        self.assertIsNotNone(avg)
        self.assertAlmostEqual(avg, 90.0, places=1)
