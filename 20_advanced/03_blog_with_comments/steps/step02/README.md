# Step 2 – Models: Tag, Post, Comment

```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

class Post(models.Model):
    STATUS = [('draft', 'Draft'), ('published', 'Published')]
    title   = models.CharField(max_length=250)
    slug    = models.SlugField(unique_for_date='publish')
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body    = models.TextField()
    tags    = models.ManyToManyField(Tag, blank=True, related_name='posts')
    status  = models.CharField(max_length=10, choices=STATUS, default='draft')
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-publish']

class Comment(models.Model):
    post   = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body   = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
