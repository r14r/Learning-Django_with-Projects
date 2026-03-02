from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    author      = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='items'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title