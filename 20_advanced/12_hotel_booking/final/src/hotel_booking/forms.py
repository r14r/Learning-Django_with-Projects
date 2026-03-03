from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['check_in', 'check_out', 'guests']
        widgets = {
            'check_in':  forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cd = super().clean()
        if cd.get('check_in') and cd.get('check_out'):
            if cd['check_out'] <= cd['check_in']:
                raise forms.ValidationError('Check-out must be after check-in.')
        return cd


class SearchForm(forms.Form):
    room_type = forms.ChoiceField(
        choices=[('', 'All')] + Booking._meta.get_field('guests').__class__._empty_choices
        if False else [('', 'All'), ('single', 'Single'), ('double', 'Double'),
                       ('suite', 'Suite'), ('deluxe', 'Deluxe')],
        required=False
    )
    capacity  = forms.IntegerField(min_value=1, required=False)
