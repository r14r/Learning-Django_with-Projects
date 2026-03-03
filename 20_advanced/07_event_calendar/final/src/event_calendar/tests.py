from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Event, Registration, Category


class EventTests(TestCase):
    def setUp(self):
        self.client    = Client()
        self.user      = User.objects.create_user('alice', password='pass')
        self.organiser = User.objects.create_user('bob', password='pass')
        self.event     = Event.objects.create(
            title='Django Meetup', slug='django-meetup',
            organiser=self.organiser, venue='Community Hall',
            start=timezone.now() + timedelta(days=7),
            end=timezone.now() + timedelta(days=7, hours=2),
        )

    def test_list_view(self):
        resp = self.client.get(reverse('event_calendar:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django Meetup')

    def test_detail_view(self):
        resp = self.client.get(
            reverse('event_calendar:detail', kwargs={'slug': 'django-meetup'})
        )
        self.assertEqual(resp.status_code, 200)

    def test_register_for_event(self):
        self.client.login(username='alice', password='pass')
        self.client.post(
            reverse('event_calendar:register', kwargs={'slug': 'django-meetup'})
        )
        self.assertEqual(Registration.objects.count(), 1)

    def test_no_duplicate_registration(self):
        self.client.login(username='alice', password='pass')
        self.client.post(
            reverse('event_calendar:register', kwargs={'slug': 'django-meetup'})
        )
        self.client.post(
            reverse('event_calendar:register', kwargs={'slug': 'django-meetup'})
        )
        self.assertEqual(Registration.objects.count(), 1)

    def test_capacity_limit(self):
        self.event.capacity = 1
        self.event.save()
        other = User.objects.create_user('carol', password='pass')
        Registration.objects.create(event=self.event, attendee=other)
        self.client.login(username='alice', password='pass')
        self.client.post(
            reverse('event_calendar:register', kwargs={'slug': 'django-meetup'})
        )
        self.assertEqual(Registration.objects.count(), 1)

    def test_cancel_registration(self):
        self.client.login(username='alice', password='pass')
        Registration.objects.create(event=self.event, attendee=self.user)
        self.client.post(
            reverse('event_calendar:cancel', kwargs={'slug': 'django-meetup'})
        )
        self.assertEqual(Registration.objects.count(), 0)
