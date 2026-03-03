from django.contrib import admin
from .models import Folder, UploadedFile


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'parent', 'created_at')


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'owner', 'folder', 'size', 'uploaded_at')
    list_filter  = ('owner',)