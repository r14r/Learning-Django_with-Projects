from django import forms
from .models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model  = Quiz
        fields = ['title', 'description']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
