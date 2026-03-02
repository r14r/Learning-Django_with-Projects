from django.contrib.auth.models import User
from django.db import models


class WeatherSearch(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    condition = models.CharField(max_length=100, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f"{self.city} - {self.condition}"
