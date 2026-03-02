from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('subject', 'name', 'email', 'is_read', 'submitted_at')
    list_filter   = ('is_read',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('submitted_at',)
