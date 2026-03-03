from django import forms
from .models import Post, Profile, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['body', 'image']
        widgets = {'body': forms.Textarea(attrs={'rows': 3})}


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['bio', 'avatar', 'website']


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'rows': 2})}