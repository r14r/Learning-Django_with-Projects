from django.contrib import admin
from .models import PageView, Event

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'method', 'user', 'timestamp')
    date_hierarchy = 'timestamp'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')