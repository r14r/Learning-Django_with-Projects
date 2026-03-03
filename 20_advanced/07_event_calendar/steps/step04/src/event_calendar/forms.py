from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model  = Event
        fields = ['title', 'slug', 'category', 'description', 'venue',
                  'start', 'end', 'capacity', 'image', 'is_public']
        widgets = {
            'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }