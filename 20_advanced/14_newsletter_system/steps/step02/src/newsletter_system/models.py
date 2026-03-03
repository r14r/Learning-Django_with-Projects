import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Subscriber(models.Model):
    email      = models.EmailField(unique=True)
    name       = models.CharField(max_length=100, blank=True)
    token      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    confirmed  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def get_confirm_url(self):
        return reverse('newsletter_system:confirm', kwargs={'token': self.token})

    def get_unsubscribe_url(self):
        return reverse('newsletter_system:unsubscribe', kwargs={'token': self.token})


class Campaign(models.Model):
    owner      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    subject    = models.CharField(max_length=300)
    body_text  = models.TextField()
    body_html  = models.TextField(blank=True)
    sent_at    = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

    @property
    def is_sent(self):
        return self.sent_at is not None
