import random
import string

from django.contrib.auth.models import User
from django.db import models


def generate_short_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=6))


class ShortURL(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=8, unique=True, default=generate_short_code)
    clicks = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"
