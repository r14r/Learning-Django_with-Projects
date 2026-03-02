from django.db import models
from django.contrib.auth.models import User


class Calculation(models.Model):
    expression = models.CharField(max_length=200)
    result     = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='calculations')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.expression} = {self.result}'
