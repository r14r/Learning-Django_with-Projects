from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['title', 'body', 'excerpt', 'published']
        widgets = {
            'title':   forms.TextInput(attrs={'class': 'form-control'}),
            'body':    forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
