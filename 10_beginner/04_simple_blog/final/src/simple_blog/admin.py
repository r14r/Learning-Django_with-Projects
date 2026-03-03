from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'published', 'created_at')
    list_filter   = ('published', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
