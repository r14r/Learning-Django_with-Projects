from django.urls import path

from . import views

app_name = 'weather'
urlpatterns = [
    path('', views.WeatherView.as_view(), name='list'),
    path('history/', views.SearchHistoryView.as_view(), name='detail'),
]
