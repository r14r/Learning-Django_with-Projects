from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    technology  = models.CharField(max_length=100)
    live_url    = models.URLField(blank=True)
    github_url  = models.URLField(blank=True)
    image       = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
