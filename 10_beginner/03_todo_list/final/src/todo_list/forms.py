from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model  = Todo
        fields = ['title', 'description', 'priority', 'due_date']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'priority':    forms.Select(attrs={'class': 'form-select'}),
            'due_date':    forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
