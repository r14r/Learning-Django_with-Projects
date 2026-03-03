from django.urls import path
from . import views

app_name = 'analytics_dashboard'
urlpatterns = [
    path('dashboard/',       views.DashboardView.as_view(), name='dashboard'),
    path('api/event/',       views.record_event,            name='event'),
    path('api/stats/daily/', views.daily_stats,             name='daily-stats'),
]