from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Post


class ExploreView(ListView):
    queryset            = Post.objects.all().select_related('author__profile')
    template_name       = 'social_network/explore.html'
    context_object_name = 'posts'
    paginate_by         = 20


def profile_view(request, username):
    target = get_object_or_404(User, username=username)
    posts  = Post.objects.filter(author=target)
    return render(request, 'social_network/profile.html', {
        'target': target, 'posts': posts,
    })


@login_required
def follow_view(request, username):
    target  = get_object_or_404(User, username=username)
    profile = request.user.profile
    if target in profile.following.all():
        profile.following.remove(target)
    else:
        profile.following.add(target)
    return redirect('social_network:profile', username=username)