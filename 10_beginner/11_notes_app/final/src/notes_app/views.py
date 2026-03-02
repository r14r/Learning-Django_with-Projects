from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import NoteForm
from .models import Note


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes_app/item_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes_app/item_detail.html'


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes_app/item_form.html'
    success_url = reverse_lazy('notes_app:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes_app/item_form.html'
    success_url = reverse_lazy('notes_app:list')


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes_app/item_confirm_delete.html'
    success_url = reverse_lazy('notes_app:list')


@login_required
def toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    if request.method == 'POST':
        note.pinned = not note.pinned
        note.save()
    return redirect('notes_app:list')
