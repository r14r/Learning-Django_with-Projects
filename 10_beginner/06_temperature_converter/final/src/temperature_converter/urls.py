from django.urls import path
from . import views

app_name = 'temperature_converter'
urlpatterns = [
    path('',        views.ConverterView.as_view(),     name='list'),
    path('history/', views.HistoryListView.as_view(),  name='detail'),
]
