from django import forms
from .models import Subscriber, Campaign


class SubscribeForm(forms.Form):
    email = forms.EmailField()
    name  = forms.CharField(max_length=100, required=False)


class CampaignForm(forms.ModelForm):
    class Meta:
        model  = Campaign
        fields = ['subject', 'body_text', 'body_html']
        widgets = {
            'body_text': forms.Textarea(attrs={'rows': 6}),
            'body_html': forms.Textarea(attrs={'rows': 10}),
        }
