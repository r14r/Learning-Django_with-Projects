from django import forms

from .models import Poll


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'description']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
