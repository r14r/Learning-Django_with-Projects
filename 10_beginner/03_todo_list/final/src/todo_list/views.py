from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm


class TodoListView(LoginRequiredMixin, ListView):
    model               = Todo
    template_name       = 'todo_list/item_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)


class TodoDetailView(LoginRequiredMixin, DetailView):
    model         = Todo
    template_name = 'todo_list/item_detail.html'


class TodoCreateView(LoginRequiredMixin, CreateView):
    model         = Todo
    form_class    = TodoForm
    template_name = 'todo_list/item_form.html'
    success_url   = reverse_lazy('todo_list:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model         = Todo
    form_class    = TodoForm
    template_name = 'todo_list/item_form.html'
    success_url   = reverse_lazy('todo_list:list')


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model         = Todo
    template_name = 'todo_list/item_confirm_delete.html'
    success_url   = reverse_lazy('todo_list:list')


@login_required
def toggle_done(request, pk):
    todo = get_object_or_404(Todo, pk=pk, author=request.user)
    if request.method == 'POST':
        todo.is_done = not todo.is_done
        todo.save()
    return redirect('todo_list:list')
