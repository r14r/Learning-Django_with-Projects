from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Item
from .forms import ItemForm


class ItemListView(ListView):
    model       = Item
    paginate_by = 10


class ItemDetailView(DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    model       = Item
    form_class  = ItemForm
    success_url = reverse_lazy('user_auth:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model       = Item
    form_class  = ItemForm
    success_url = reverse_lazy('user_auth:list')


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model       = Item
    success_url = reverse_lazy('user_auth:list')
