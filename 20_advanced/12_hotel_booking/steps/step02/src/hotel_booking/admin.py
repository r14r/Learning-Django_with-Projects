from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display  = ('number', 'room_type', 'capacity', 'price_night', 'available')
    list_filter   = ('room_type', 'available')
    list_editable = ('available',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'room', 'guest', 'check_in', 'check_out', 'status')
    list_filter  = ('status',)