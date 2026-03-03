from django.contrib import admin

from .models import WeatherSearch


@admin.register(WeatherSearch)
class WeatherSearchAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'condition', 'humidity', 'user', 'searched_at')
    list_filter = ('condition',)
    search_fields = ('city', 'condition')
