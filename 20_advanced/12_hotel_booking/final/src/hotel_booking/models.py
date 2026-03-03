from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'), ('double', 'Double'),
        ('suite', 'Suite'), ('deluxe', 'Deluxe'),
    ]
    number      = models.CharField(max_length=10, unique=True)
    room_type   = models.CharField(max_length=10, choices=ROOM_TYPES, default='single')
    capacity    = models.PositiveIntegerField(default=2)
    price_night = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    amenities   = models.TextField(blank=True)
    image       = models.ImageField(upload_to='rooms/', blank=True)
    available   = models.BooleanField(default=True)

    def __str__(self):
        return f'Room {self.number} ({self.get_room_type_display()})'

    def get_absolute_url(self):
        return reverse('hotel_booking:room-detail', kwargs={'pk': self.pk})


class Booking(models.Model):
    STATUS = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')]

    room        = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in    = models.DateField()
    check_out   = models.DateField()
    guests      = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    status      = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Booking {self.pk}: {self.guest.username} @ Room {self.room.number}'

    @property
    def nights(self):
        return (self.check_out - self.check_in).days
