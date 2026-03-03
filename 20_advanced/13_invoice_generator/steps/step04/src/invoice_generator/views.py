from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Client as InvoiceClient, Invoice, LineItem
from .forms import InvoiceForm, ClientForm

LineItemFormSet = inlineformset_factory(
    Invoice, LineItem,
    fields=['description', 'quantity', 'unit_price', 'order'],
    extra=3, can_delete=True,
)


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


@login_required
def invoice_create(request):
    if request.method == 'POST':
        form    = InvoiceForm(request.POST)
        formset = LineItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice        = form.save(commit=False)
            invoice.owner  = request.user
            invoice.save()
            formset.instance = invoice
            formset.save()
            return redirect(invoice.get_absolute_url())
    else:
        form    = InvoiceForm()
        formset = LineItemFormSet()
    return render(request, 'invoice_generator/invoice_form.html', {'form': form, 'formset': formset})


@login_required
def update_status(request, pk, status):
    invoice = get_object_or_404(Invoice, pk=pk, owner=request.user)
    if status in dict(Invoice.STATUS):
        invoice.status = status
        invoice.save()
    return redirect('invoice_generator:detail', pk=pk)