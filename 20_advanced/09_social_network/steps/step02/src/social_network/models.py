from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio       = models.TextField(blank=True)
    avatar    = models.ImageField(upload_to='avatars/', blank=True)
    website   = models.URLField(blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def get_absolute_url(self):
        return reverse('social_network:profile', kwargs={'username': self.user.username})


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Post(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body       = models.TextField()
    image      = models.ImageField(upload_to='posts/', blank=True)
    likes      = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username}: {self.body[:40]}'

    @property
    def like_count(self):
        return self.likes.count()


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} on post {self.post_id}'
