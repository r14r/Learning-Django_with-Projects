from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Task, TaskComment
from .forms import TaskForm, CommentForm


class TaskListView(LoginRequiredMixin, ListView):
    model               = Task
    template_name       = 'task_manager/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user).select_related('assignee')
        status   = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        return qs


class TaskDetailView(LoginRequiredMixin, DetailView):
    model         = Task
    template_name = 'task_manager/task_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        ctx['comments']     = self.object.comments.select_related('author')
        return ctx


class TaskCreateView(LoginRequiredMixin, CreateView):
    model         = Task
    form_class    = TaskForm
    template_name = 'task_manager/task_form.html'
    success_url   = reverse_lazy('task_manager:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model         = Task
    form_class    = TaskForm
    template_name = 'task_manager/task_form.html'
    success_url   = reverse_lazy('task_manager:list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model         = Task
    template_name = 'task_manager/task_confirm_delete.html'
    success_url   = reverse_lazy('task_manager:list')


@login_required
def update_status(request, pk, status):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if status in dict(Task.STATUS):
        task.status = status
        task.save()
    return redirect('task_manager:list')


@login_required
def board_view(request):
    base = Task.objects.filter(owner=request.user)
    return render(request, 'task_manager/board.html', {
        'todo':        base.filter(status='todo'),
        'in_progress': base.filter(status='in_progress'),
        'done':        base.filter(status='done'),
    })


@login_required
def add_comment(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c        = form.save(commit=False)
            c.task   = task
            c.author = request.user
            c.save()
    return redirect('task_manager:detail', pk=pk)