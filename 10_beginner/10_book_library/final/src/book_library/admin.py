from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author_name', 'genre', 'published_year', 'available')
    list_filter   = ('available', 'genre')
    search_fields = ('title', 'author_name', 'isbn')
