import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


def generate_number():
    return f'INV-{uuid.uuid4().hex[:8].upper()}'


class Client(models.Model):
    owner   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    address = models.TextField(blank=True)
    tax_id  = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS = [('draft', 'Draft'), ('sent', 'Sent'), ('paid', 'Paid')]

    owner      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    client     = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    number     = models.CharField(max_length=20, unique=True, default=generate_number)
    issue_date = models.DateField()
    due_date   = models.DateField()
    status     = models.CharField(max_length=10, choices=STATUS, default='draft')
    tax_rate   = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.20'))
    notes      = models.TextField(blank=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f'Invoice {self.number}'

    def get_absolute_url(self):
        return reverse('invoice_generator:detail', kwargs={'pk': self.pk})

    @property
    def subtotal(self):
        return sum(i.total for i in self.items.all())

    @property
    def tax_amount(self):
        return self.subtotal * self.tax_rate

    @property
    def total(self):
        return self.subtotal + self.tax_amount


class LineItem(models.Model):
    invoice     = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=300)
    quantity    = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1'))
    unit_price  = models.DecimalField(max_digits=10, decimal_places=2)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return self.description
