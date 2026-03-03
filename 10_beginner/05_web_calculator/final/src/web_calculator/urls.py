from django.urls import path
from . import views

app_name = 'web_calculator'
urlpatterns = [
    path('',        views.CalculatorView.as_view(),   name='list'),
    path('history/', views.HistoryListView.as_view(), name='detail'),
]
