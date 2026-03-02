from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
        }