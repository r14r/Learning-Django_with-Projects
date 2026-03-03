from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Tag, Comment
from .forms import CommentForm


class PostListView(ListView):
    template_name       = 'blog_with_comments/post_list.html'
    context_object_name = 'posts'
    paginate_by         = 5

    def get_queryset(self):
        qs = Post.published.all().prefetch_related('tags', 'author')
        slug = self.kwargs.get('slug')
        if slug:
            tag = get_object_or_404(Tag, slug=slug)
            qs  = qs.filter(tags=tag)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tags'] = Tag.objects.all()
        slug = self.kwargs.get('slug')
        if slug:
            ctx['active_tag'] = get_object_or_404(Tag, slug=slug)
        return ctx


def post_detail(request, year, month, day, slug):
    post     = get_object_or_404(Post, publish__year=year, publish__month=month,
                                 publish__day=day, slug=slug, status='published')
    comments = post.comments.filter(active=True).select_related('author')
    form     = None
    if request.user.is_authenticated:
        form = CommentForm()
    related = (Post.published.filter(tags__in=post.tags.all())
               .exclude(pk=post.pk).distinct()[:3])
    return render(request, 'blog_with_comments/post_detail.html', {
        'post': post, 'comments': comments, 'form': form, 'related': related,
    })


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment        = form.save(commit=False)
            comment.post   = post
            comment.author = request.user
            comment.save()
    return redirect(post.get_absolute_url())
