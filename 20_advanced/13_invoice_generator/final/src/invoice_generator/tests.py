from django.test import TestCase, Client as TestClient
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date
from .models import Client as InvoiceClient, Invoice, LineItem


class InvoiceTests(TestCase):
    def setUp(self):
        self.client   = TestClient()
        self.user     = User.objects.create_user('alice', password='pass')
        self.client.login(username='alice', password='pass')
        self.cli      = InvoiceClient.objects.create(
            owner=self.user, name='Acme Corp', email='a@acme.com'
        )
        self.invoice  = Invoice.objects.create(
            owner=self.user, client=self.cli,
            issue_date=date.today(), due_date=date.today(),
        )
        self.line     = LineItem.objects.create(
            invoice=self.invoice, description='Web Dev',
            quantity=Decimal('10'), unit_price=Decimal('100'),
        )

    def test_subtotal(self):
        self.assertEqual(self.invoice.subtotal, Decimal('1000'))

    def test_total_with_tax(self):
        expected = Decimal('1000') * Decimal('1.20')
        self.assertEqual(self.invoice.total, expected)

    def test_invoice_list(self):
        resp = self.client.get(reverse('invoice_generator:list'))
        self.assertEqual(resp.status_code, 200)

    def test_invoice_detail(self):
        resp = self.client.get(
            reverse('invoice_generator:detail', kwargs={'pk': self.invoice.pk})
        )
        self.assertEqual(resp.status_code, 200)

    def test_mark_sent(self):
        self.client.post(
            reverse('invoice_generator:update-status',
                    kwargs={'pk': self.invoice.pk, 'status': 'sent'})
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'sent')

    def test_mark_paid(self):
        self.invoice.status = 'sent'
        self.invoice.save()
        self.client.post(
            reverse('invoice_generator:update-status',
                    kwargs={'pk': self.invoice.pk, 'status': 'paid'})
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'paid')