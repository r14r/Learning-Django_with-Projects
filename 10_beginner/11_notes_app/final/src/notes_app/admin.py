from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pinned', 'updated_at')
    list_filter = ('pinned', 'author')
    search_fields = ('title', 'content')
