from .models import Item
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ItemForm

class ItemCreateView(LoginRequiredMixin, CreateView):
    model      = Item
    form_class = ItemForm
    success_url = reverse_lazy('rest_api:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model      = Item
    form_class = ItemForm
    success_url = reverse_lazy('rest_api:list')

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model       = Item
    success_url = reverse_lazy('rest_api:list')