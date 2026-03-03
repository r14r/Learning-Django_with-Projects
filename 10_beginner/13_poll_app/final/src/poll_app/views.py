from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import PollForm
from .models import Choice, Poll


class PollListView(ListView):
    model = Poll
    template_name = 'poll_app/item_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Poll.objects.filter(is_active=True)


class PollDetailView(DetailView):
    model = Poll
    template_name = 'poll_app/item_detail.html'


class VoteView(View):
    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, pk=choice_id, poll=poll)
            choice.votes += 1
            choice.save()
        return redirect('poll_app:detail', pk=pk)


class PollCreateView(LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = 'poll_app/item_form.html'
    success_url = reverse_lazy('poll_app:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PollDeleteView(LoginRequiredMixin, DeleteView):
    model = Poll
    template_name = 'poll_app/item_confirm_delete.html'
    success_url = reverse_lazy('poll_app:list')
