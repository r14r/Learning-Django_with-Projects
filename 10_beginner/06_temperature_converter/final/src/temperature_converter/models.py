from django.db import models
from django.contrib.auth.models import User


UNIT_CHOICES = [
    ('C', 'Celsius'),
    ('F', 'Fahrenheit'),
    ('K', 'Kelvin'),
]


class Conversion(models.Model):
    value_in   = models.DecimalField(max_digits=10, decimal_places=4)
    unit_in    = models.CharField(max_length=10, choices=UNIT_CHOICES)
    value_out  = models.DecimalField(max_digits=10, decimal_places=4)
    unit_out   = models.CharField(max_length=10, choices=UNIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    user       = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.value_in}{self.unit_in} → {self.value_out}{self.unit_out}"
