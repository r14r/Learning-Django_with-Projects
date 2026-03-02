from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title          = models.CharField(max_length=300)
    author_name    = models.CharField(max_length=200)
    isbn           = models.CharField(max_length=13, blank=True)
    genre          = models.CharField(max_length=100, blank=True)
    published_year = models.PositiveIntegerField(null=True, blank=True)
    description    = models.TextField(blank=True)
    cover          = models.ImageField(upload_to='covers/', blank=True, null=True)
    available      = models.BooleanField(default=True)
    added_by       = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author_name}"
