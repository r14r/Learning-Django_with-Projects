from django import forms

from .models import ShortURL


class URLShortenForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/long/url'}),
        }
        labels = {
            'original_url': 'URL to shorten',
        }
