from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model  = Job
        fields = ['title', 'description', 'location', 'job_type', 'salary_min', 'salary_max', 'is_active']
        widgets = {'description': forms.Textarea(attrs={'rows': 6})}


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['cover_letter', 'resume']
        widgets = {'cover_letter': forms.Textarea(attrs={'rows': 5})}