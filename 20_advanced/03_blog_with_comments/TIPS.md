# Tips & Implementation Guide: Blog with Comments

## 1. Post Model with Status

```python
class Post(models.Model):
    STATUS = [('draft', 'Draft'), ('published', 'Published')]
    title   = models.CharField(max_length=250)
    slug    = models.SlugField(unique_for_date='publish')
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body    = models.TextField()
    tags    = models.ManyToManyField('Tag', blank=True, related_name='posts')
    status  = models.CharField(max_length=10, choices=STATUS, default='draft')
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish']

    objects = models.Manager()
    published = PublishedManager()  # custom manager filtering status='published'
```

## 2. Custom Manager

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')
```

## 3. Comment Form

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['body']
```

## 4. Post Detail View with Comment Handling

```python
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, publish__year=year, publish__month=month,
                             publish__day=day, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post   = post
                comment.author = request.user
                comment.save()
                return redirect(post.get_absolute_url())
        else:
            form = CommentForm()
    related = Post.published.filter(tags__in=post.tags.all()).exclude(pk=post.pk).distinct()[:3]
    return render(request, 'blog_with_comments/post_detail.html', {
        'post': post, 'comments': comments, 'form': form, 'related': related,
    })
```
