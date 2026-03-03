from django.contrib import admin
from .models import Subscriber, Campaign

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display  = ('email', 'name', 'confirmed', 'created_at')
    list_filter   = ('confirmed',)
    search_fields = ('email', 'name')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner', 'sent_at', 'created_at')