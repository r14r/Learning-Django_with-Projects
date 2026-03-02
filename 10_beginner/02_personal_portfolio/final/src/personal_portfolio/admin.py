from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'technology', 'author', 'created_at')
    list_filter   = ('technology',)
    search_fields = ('title', 'description', 'technology')
