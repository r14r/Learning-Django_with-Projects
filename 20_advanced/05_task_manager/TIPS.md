# Tips & Implementation Guide: Advanced Task Manager

## 1. Model with Priority and Status

```python
class Task(models.Model):
    STATUS   = [('todo','Todo'),('in_progress','In Progress'),('done','Done')]
    PRIORITY = [('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')]

    title       = models.CharField(max_length=200)
    status      = models.CharField(max_length=20, choices=STATUS, default='todo')
    priority    = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    due_date    = models.DateField(null=True, blank=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    assignee    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tasks')
    labels      = models.ManyToManyField('Label', blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date and self.due_date < timezone.now().date() and self.status != 'done'
```

## 2. Filtering with django-filter

```python
# filters.py
import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model  = Task
        fields = {'status': ['exact'], 'priority': ['exact'], 'assignee': ['exact']}
```

## 3. Kanban Board View

```python
def board_view(request):
    tasks = Task.objects.filter(owner=request.user)
    ctx = {
        'todo':        tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'done':        tasks.filter(status='done'),
    }
    return render(request, 'task_manager/board.html', ctx)
```

## 4. Quick Status Update

```python
@login_required
def update_status(request, pk, status):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if status in dict(Task.STATUS):
        task.status = status
        task.save()
    return redirect('task_manager:list')
```
