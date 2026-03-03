from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Profile, Post, Comment
from .forms import PostForm, ProfileForm, CommentForm


class FeedView(LoginRequiredMixin, ListView):
    template_name       = 'social_network/feed.html'
    context_object_name = 'posts'
    paginate_by         = 20

    def get_queryset(self):
        following = self.request.user.profile.following.all()
        authors   = list(following) + [self.request.user]
        return Post.objects.filter(author__in=authors).select_related(
            'author__profile'
        ).prefetch_related('likes', 'comments')


class ExploreView(ListView):
    queryset            = Post.objects.all().select_related('author__profile')
    template_name       = 'social_network/explore.html'
    context_object_name = 'posts'
    paginate_by         = 20


def profile_view(request, username):
    target   = get_object_or_404(User, username=username)
    posts    = Post.objects.filter(author=target)
    is_following = (request.user.is_authenticated and
                    target in request.user.profile.following.all())
    return render(request, 'social_network/profile.html', {
        'target': target, 'posts': posts, 'is_following': is_following,
    })


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model         = Profile
    form_class    = ProfileForm
    template_name = 'social_network/profile_edit.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('social_network:profile',
                            kwargs={'username': self.request.user.username})


class PostCreateView(LoginRequiredMixin, CreateView):
    model         = Post
    form_class    = PostForm
    template_name = 'social_network/post_form.html'
    success_url   = reverse_lazy('social_network:feed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model         = Post
    template_name = 'social_network/post_confirm_delete.html'
    success_url   = reverse_lazy('social_network:feed')


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', reverse_lazy('social_network:feed')))


@login_required
def follow_view(request, username):
    target  = get_object_or_404(User, username=username)
    profile = request.user.profile
    if target in profile.following.all():
        profile.following.remove(target)
    else:
        profile.following.add(target)
    return redirect('social_network:profile', username=username)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c        = form.save(commit=False)
            c.post   = post
            c.author = request.user
            c.save()
    return redirect(request.META.get('HTTP_REFERER', reverse_lazy('social_network:feed')))
