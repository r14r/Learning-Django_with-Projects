from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model  = Project
        fields = ['title', 'description', 'technology', 'live_url', 'github_url', 'image']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'technology':  forms.TextInput(attrs={'class': 'form-control'}),
            'live_url':    forms.URLInput(attrs={'class': 'form-control'}),
            'github_url':  forms.URLInput(attrs={'class': 'form-control'}),
        }
