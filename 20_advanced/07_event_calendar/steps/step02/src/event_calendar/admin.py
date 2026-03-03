from django.contrib import admin
from .models import Category, Event, Registration


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ('title', 'organiser', 'start', 'capacity', 'is_public')
    list_filter   = ('is_public', 'category')
    search_fields = ('title', 'venue')


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee', 'created_at')