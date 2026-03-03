from django import forms
from .models import Invoice, Client as InvoiceClient


class ClientForm(forms.ModelForm):
    class Meta:
        model  = InvoiceClient
        fields = ['name', 'email', 'address', 'tax_id']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model  = Invoice
        fields = ['client', 'issue_date', 'due_date', 'tax_rate', 'notes']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date':   forms.DateInput(attrs={'type': 'date'}),
        }
