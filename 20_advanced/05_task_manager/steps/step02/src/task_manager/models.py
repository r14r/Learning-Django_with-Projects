from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Label(models.Model):
    name  = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6c757d')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labels')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS   = [('todo', 'Todo'), ('in_progress', 'In Progress'), ('done', 'Done')]
    PRIORITY = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')]

    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS, default='todo')
    priority    = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    due_date    = models.DateField(null=True, blank=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    assignee    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tasks')
    labels      = models.ManyToManyField(Label, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_manager:detail', kwargs={'pk': self.pk})

    @property
    def is_overdue(self):
        return (self.due_date and
                self.due_date < timezone.now().date() and
                self.status != 'done')


class TaskComment(models.Model):
    task       = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} on task {self.task_id}'
