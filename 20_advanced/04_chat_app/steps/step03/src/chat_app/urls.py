from django.urls import path
from . import views

app_name = 'chat_app'
urlpatterns = [
    path('',                   views.RoomListView.as_view(), name='list'),
    path('room/<slug:slug>/',  views.room_view,              name='room'),
]