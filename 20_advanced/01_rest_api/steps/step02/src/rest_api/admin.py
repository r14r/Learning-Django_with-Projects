from django.contrib import admin
from .models import Author, Book, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display  = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'genre', 'published', 'owner')
    list_filter   = ('genre', 'published')
    search_fields = ('title', 'author__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('book', 'author', 'rating', 'created_at')
    list_filter   = ('rating',)
