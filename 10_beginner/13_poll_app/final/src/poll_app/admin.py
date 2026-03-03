from django.contrib import admin

from .models import Choice, Poll


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'is_active', 'created_at')
    list_filter = ('is_active', 'author')
    search_fields = ('question', 'description')
    inlines = [ChoiceInline]
