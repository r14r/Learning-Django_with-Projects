from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = ['first_name', 'last_name', 'email', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=50, initial=1)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
