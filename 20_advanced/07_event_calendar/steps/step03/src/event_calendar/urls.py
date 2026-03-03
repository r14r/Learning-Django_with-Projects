from django.urls import path
from . import views

app_name = 'event_calendar'
urlpatterns = [
    path('',                    views.UpcomingEventsView.as_view(), name='list'),
    path('event/<slug:slug>/',  views.EventDetailView.as_view(),    name='detail'),
]