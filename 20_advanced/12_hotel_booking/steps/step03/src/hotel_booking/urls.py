from django.urls import path
from . import views

app_name = 'hotel_booking'
urlpatterns = [
    path('',             views.RoomListView.as_view(),   name='list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
]