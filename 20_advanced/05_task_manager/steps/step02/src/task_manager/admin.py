from django.contrib import admin
from .models import Label, Task, TaskComment


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'owner')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display   = ('title', 'owner', 'status', 'priority', 'due_date')
    list_filter    = ('status', 'priority')
    search_fields  = ('title',)
    filter_horizontal = ('labels',)


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')