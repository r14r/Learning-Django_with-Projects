from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date, timedelta
from .models import Room, Booking


class HotelBookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user   = User.objects.create_user('alice', password='pass')
        self.room   = Room.objects.create(
            number='101', room_type='double', capacity=2,
            price_night=Decimal('99.00')
        )

    def _check_in(self, delta=1):
        return date.today() + timedelta(days=delta)

    def _check_out(self, delta=3):
        return date.today() + timedelta(days=delta)

    def test_room_list(self):
        resp = self.client.get(reverse('hotel_booking:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Room 101')

    def test_book_requires_login(self):
        resp = self.client.post(reverse('hotel_booking:book', kwargs={'pk': self.room.pk}))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_booking(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('hotel_booking:book', kwargs={'pk': self.room.pk}), {
            'check_in': self._check_in(), 'check_out': self._check_out(), 'guests': 2,
        })
        self.assertEqual(Booking.objects.count(), 1)

    def test_total_price_computed(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('hotel_booking:book', kwargs={'pk': self.room.pk}), {
            'check_in': self._check_in(), 'check_out': self._check_out(), 'guests': 1,
        })
        b = Booking.objects.first()
        self.assertEqual(b.total_price, Decimal('198.00'))

    def test_no_double_booking(self):
        other = User.objects.create_user('bob', password='pass')
        Booking.objects.create(
            room=self.room, guest=other,
            check_in=self._check_in(), check_out=self._check_out(),
            status='confirmed', total_price=Decimal('198'),
        )
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('hotel_booking:book', kwargs={'pk': self.room.pk}), {
            'check_in': self._check_in(), 'check_out': self._check_out(), 'guests': 1,
        })
        self.assertEqual(Booking.objects.filter(guest=self.user).count(), 0)

    def test_cancel_booking(self):
        b = Booking.objects.create(
            room=self.room, guest=self.user,
            check_in=self._check_in(), check_out=self._check_out(),
            status='pending', total_price=Decimal('198'),
        )
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('hotel_booking:cancel', kwargs={'pk': b.pk}))
        b.refresh_from_db()
        self.assertEqual(b.status, 'cancelled')
