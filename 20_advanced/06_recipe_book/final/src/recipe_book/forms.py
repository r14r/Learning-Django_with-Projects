from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model  = Recipe
        fields = ['title', 'slug', 'categories', 'description', 'image',
                  'prep_time', 'cook_time', 'servings', 'instructions', 'published']
        widgets = {
            'description':  forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 8}),
        }
