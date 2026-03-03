from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'created_at')
    list_filter   = ('author',)
    search_fields = ('title', 'body')
