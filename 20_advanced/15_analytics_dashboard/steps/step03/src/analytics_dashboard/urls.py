from django.urls import path
from . import views

app_name = 'analytics_dashboard'
urlpatterns = [
    path('api/event/', views.record_event, name='event'),
]