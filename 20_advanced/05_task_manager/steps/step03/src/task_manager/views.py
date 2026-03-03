from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model               = Task
    template_name       = 'task_manager/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).select_related('assignee')


class TaskDetailView(LoginRequiredMixin, DetailView):
    model         = Task
    template_name = 'task_manager/task_detail.html'


@login_required
def board_view(request):
    base = Task.objects.filter(owner=request.user)
    return render(request, 'task_manager/board.html', {
        'todo':        base.filter(status='todo'),
        'in_progress': base.filter(status='in_progress'),
        'done':        base.filter(status='done'),
    })