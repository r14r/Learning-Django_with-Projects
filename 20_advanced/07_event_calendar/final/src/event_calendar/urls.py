from django.urls import path
from . import views

app_name = 'event_calendar'
urlpatterns = [
    path('',                           views.UpcomingEventsView.as_view(), name='list'),
    path('event/<slug:slug>/',         views.EventDetailView.as_view(),    name='detail'),
    path('event/create/',              views.EventCreateView.as_view(),    name='create'),
    path('event/<slug:slug>/edit/',    views.EventUpdateView.as_view(),    name='update'),
    path('event/<slug:slug>/delete/',  views.EventDeleteView.as_view(),    name='delete'),
    path('event/<slug:slug>/register/', views.register_view,              name='register'),
    path('event/<slug:slug>/cancel/',  views.cancel_view,                  name='cancel'),
    path('my-events/',                 views.MyEventsView.as_view(),       name='my-events'),
]
