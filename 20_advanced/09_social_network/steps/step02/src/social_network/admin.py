from django.contrib import admin
from .models import Profile, Post, Comment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_at')
    list_filter  = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')