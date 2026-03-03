from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_done     = models.BooleanField(default=False)
    priority    = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date    = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    class Meta:
        ordering = ['is_done', '-priority', 'due_date']

    def __str__(self):
        return self.title
