from django import forms
from .models import Task, TaskComment


class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assignee', 'labels']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date':    forms.DateInput(attrs={'type': 'date'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model  = TaskComment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'rows': 2})}