from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Company, Job, Application


class JobBoardTests(TestCase):
    def setUp(self):
        self.client    = Client()
        self.employer  = User.objects.create_user('employer', password='pass')
        self.seeker    = User.objects.create_user('seeker', password='pass')
        self.company   = Company.objects.create(owner=self.employer, name='Acme Corp')
        self.job       = Job.objects.create(
            company=self.company, title='Django Developer',
            description='Build Django apps', location='Berlin', job_type='full_time',
        )

    def test_job_list(self):
        resp = self.client.get(reverse('job_board:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django Developer')

    def test_job_detail(self):
        resp = self.client.get(reverse('job_board:detail', kwargs={'pk': self.job.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_apply_requires_login(self):
        resp = self.client.post(reverse('job_board:apply', kwargs={'pk': self.job.pk}))
        self.assertNotEqual(resp.status_code, 200)

    def test_apply_to_job(self):
        self.client.login(username='seeker', password='pass')
        self.client.post(reverse('job_board:apply', kwargs={'pk': self.job.pk}), {
            'cover_letter': 'I am a great Django developer.'
        })
        self.assertEqual(Application.objects.count(), 1)

    def test_no_duplicate_application(self):
        self.client.login(username='seeker', password='pass')
        for _ in range(2):
            self.client.post(reverse('job_board:apply', kwargs={'pk': self.job.pk}), {
                'cover_letter': 'Me!'
            })
        self.assertEqual(Application.objects.count(), 1)

    def test_employer_dashboard(self):
        self.client.login(username='employer', password='pass')
        resp = self.client.get(reverse('job_board:employer-dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django Developer')

    def test_update_application_status(self):
        Application.objects.create(job=self.job, applicant=self.seeker, cover_letter='...')
        self.client.login(username='employer', password='pass')
        app = Application.objects.first()
        self.client.post(
            reverse('job_board:update-status', kwargs={'pk': app.pk, 'status': 'accepted'})
        )
        app.refresh_from_db()
        self.assertEqual(app.status, 'accepted')
