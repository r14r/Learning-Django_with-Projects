from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm


class BookListView(ListView):
    model               = Book
    template_name       = 'book_library/item_list.html'
    context_object_name = 'books'
    paginate_by         = 12

    def get_queryset(self):
        qs = super().get_queryset()
        genre = self.request.GET.get('genre', '').strip()
        if genre:
            qs = qs.filter(genre__iexact=genre)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['genre_filter'] = self.request.GET.get('genre', '')
        ctx['genres'] = Book.objects.exclude(genre='').values_list('genre', flat=True).distinct()
        return ctx


class BookDetailView(DetailView):
    model               = Book
    template_name       = 'book_library/item_detail.html'
    context_object_name = 'book'


class BookCreateView(LoginRequiredMixin, CreateView):
    model         = Book
    form_class    = BookForm
    template_name = 'book_library/item_form.html'
    success_url   = reverse_lazy('book_library:list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model         = Book
    form_class    = BookForm
    template_name = 'book_library/item_form.html'
    success_url   = reverse_lazy('book_library:list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model         = Book
    template_name = 'book_library/item_confirm_delete.html'
    success_url   = reverse_lazy('book_library:list')
