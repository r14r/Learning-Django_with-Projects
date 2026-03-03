from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name  = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Event(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    organiser   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organised_events')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='events')
    description = models.TextField(blank=True)
    venue       = models.CharField(max_length=200)
    start       = models.DateTimeField()
    end         = models.DateTimeField()
    capacity    = models.PositiveIntegerField(default=0, help_text='0 = unlimited')
    image       = models.ImageField(upload_to='events/', blank=True)
    is_public   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_calendar:detail', kwargs={'slug': self.slug})

    @property
    def is_full(self):
        return self.capacity > 0 and self.registrations.count() >= self.capacity

    @property
    def spots_left(self):
        if self.capacity == 0:
            return None
        return self.capacity - self.registrations.count()


class Registration(models.Model):
    event      = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    attendee   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'attendee')

    def __str__(self):
        return f'{self.attendee.username} @ {self.event.title}'
