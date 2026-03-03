# Step 4 – Comment Form & Tag Filtering

## blog_with_comments/forms.py

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'rows': 4})}
```
