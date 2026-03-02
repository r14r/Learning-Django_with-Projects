from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display  = ('title', 'priority', 'is_done', 'due_date', 'author')
    list_filter   = ('priority', 'is_done', 'author')
    search_fields = ('title',)
