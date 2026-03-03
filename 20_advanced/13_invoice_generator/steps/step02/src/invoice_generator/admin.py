from django.contrib import admin
from .models import Client as InvoiceClient, Invoice, LineItem

admin.site.register(InvoiceClient)

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 2

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'status', 'issue_date', 'due_date')
    list_filter  = ('status',)
    inlines      = [LineItemInline]