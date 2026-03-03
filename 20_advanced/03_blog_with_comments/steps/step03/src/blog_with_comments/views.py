from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from .models import Post, Tag


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
        return ctx


def post_detail(request, year, month, day, slug):
    post     = get_object_or_404(Post, publish__year=year, publish__month=month,
                                 publish__day=day, slug=slug, status='published')
    comments = post.comments.filter(active=True).select_related('author')
    return render(request, 'blog_with_comments/post_detail.html', {
        'post': post, 'comments': comments,
    })