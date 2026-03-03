from django.db import models
from django.contrib.auth.models import User


class PageView(models.Model):
    path        = models.CharField(max_length=500)
    method      = models.CharField(max_length=10, default='GET')
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    user_agent  = models.TextField(blank=True)
    referer     = models.URLField(blank=True, max_length=2000)
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.path} @ {self.timestamp}'


class Event(models.Model):
    name        = models.CharField(max_length=100)
    properties  = models.JSONField(default=dict)
    session_key = models.CharField(max_length=40, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.name
