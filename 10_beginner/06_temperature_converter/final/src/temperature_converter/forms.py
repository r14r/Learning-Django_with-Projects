from django import forms
from .models import UNIT_CHOICES


class ConverterForm(forms.Form):
    value_in = forms.DecimalField(
        max_digits=10, decimal_places=4,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Enter value'}),
        label='Value',
    )
    unit_in = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='From',
    )
    unit_out = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='To',
    )
