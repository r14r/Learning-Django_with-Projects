from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Message
from .forms import MessageForm


class MessageListView(ListView):
    model       = Message
    paginate_by = 10
    template_name = 'hello_django/item_list.html'
    context_object_name = 'object_list'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'hello_django/item_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model      = Message
    form_class = MessageForm
    template_name = 'hello_django/item_form.html'
    success_url = reverse_lazy('hello_django:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model      = Message
    form_class = MessageForm
    template_name = 'hello_django/item_form.html'
    success_url = reverse_lazy('hello_django:list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model       = Message
    template_name = 'hello_django/item_confirm_delete.html'
    success_url = reverse_lazy('hello_django:list')
