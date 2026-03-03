from django.contrib import admin
from .models import Conversion


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display  = ('value_in', 'unit_in', 'value_out', 'unit_out', 'user', 'created_at')
    list_filter   = ('unit_in', 'unit_out')
    search_fields = ('user__username',)
