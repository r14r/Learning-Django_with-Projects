from django import forms


class CalculatorForm(forms.Form):
    expression = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':       'form-control form-control-lg',
            'placeholder': 'e.g. 2 + 3 * (4 - 1)',
            'autofocus':   True,
        })
    )
