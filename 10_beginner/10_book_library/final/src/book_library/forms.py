from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model  = Book
        fields = ['title', 'author_name', 'isbn', 'genre', 'published_year',
                  'description', 'cover', 'available']
        widgets = {
            'title':          forms.TextInput(attrs={'class': 'form-control'}),
            'author_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'isbn':           forms.TextInput(attrs={'class': 'form-control'}),
            'genre':          forms.TextInput(attrs={'class': 'form-control'}),
            'published_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'description':    forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
