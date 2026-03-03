# Tips & Implementation Guide: Social Network

## 1. Auto-Create Profile with Signal

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

## 2. Follow System

Use a ManyToManyField on Profile pointing to User:

```python
class Profile(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
```

Follow view:
```python
@login_required
def follow_view(request, username):
    target = get_object_or_404(User, username=username)
    profile = request.user.profile
    if target in profile.following.all():
        profile.following.remove(target)
    else:
        profile.following.add(target)
    return redirect('social_network:profile', username=username)
```

## 3. Personalised Feed

```python
class FeedView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        following = request.user.profile.following.all()
        return Post.objects.filter(
            author__in=list(following) + [request.user]
        ).select_related('author__profile').prefetch_related('likes')
```

## 4. Like Toggle

```python
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'social_network:feed'))
```
