from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_with_comments:tag', kwargs={'slug': self.slug})


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS = [('draft', 'Draft'), ('published', 'Published')]

    title      = models.CharField(max_length=250)
    slug       = models.SlugField(unique_for_date='publish')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body       = models.TextField()
    image      = models.ImageField(upload_to='posts/', blank=True)
    tags       = models.ManyToManyField(Tag, blank=True, related_name='posts')
    status     = models.CharField(max_length=10, choices=STATUS, default='draft')
    publish    = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    objects  = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_with_comments:detail', kwargs={
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day,
            'slug': self.slug,
        })


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'
