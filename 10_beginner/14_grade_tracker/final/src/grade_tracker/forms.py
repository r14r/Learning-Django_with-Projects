from django import forms

from .models import Course, Grade


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['assignment', 'score', 'max_score']
        widgets = {
            'assignment': forms.TextInput(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
