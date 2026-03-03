# Step 3 – List & Detail Views with Pagination

## blog_with_comments/views.py

```python
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, Comment
from .forms import CommentForm

class PostListView(ListView):
    queryset    = Post.published.all().prefetch_related('tags')
    template_name = 'blog_with_comments/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
        publish__year=year, publish__month=month,
        publish__day=day, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    ...
```
