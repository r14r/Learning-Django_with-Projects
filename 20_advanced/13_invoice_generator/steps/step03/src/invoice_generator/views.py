from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client as InvoiceClient, Invoice


class InvoiceListView(LoginRequiredMixin, ListView):
    template_name       = 'invoice_generator/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.filter(owner=self.request.user).select_related('client')


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model         = Invoice
    template_name = 'invoice_generator/invoice_detail.html'


class ClientListView(LoginRequiredMixin, ListView):
    template_name       = 'invoice_generator/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return InvoiceClient.objects.filter(owner=self.request.user)