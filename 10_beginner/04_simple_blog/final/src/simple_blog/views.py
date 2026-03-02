from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model               = Post
    template_name       = 'simple_blog/item_list.html'
    context_object_name = 'object_list'
    paginate_by         = 10
    queryset            = Post.objects.filter(published=True)


class PostDetailView(DetailView):
    model         = Post
    template_name = 'simple_blog/item_detail.html'
    slug_field    = 'slug'
    slug_url_kwarg = 'slug'


class PostCreateView(LoginRequiredMixin, CreateView):
    model         = Post
    form_class    = PostForm
    template_name = 'simple_blog/item_form.html'
    success_url   = reverse_lazy('simple_blog:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model         = Post
    form_class    = PostForm
    template_name = 'simple_blog/item_form.html'
    success_url   = reverse_lazy('simple_blog:list')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model         = Post
    template_name = 'simple_blog/item_confirm_delete.html'
    success_url   = reverse_lazy('simple_blog:list')
