from django.urls import path
from . import views

app_name = 'job_board'
urlpatterns = [
    path('',             views.JobListView.as_view(),   name='list'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='detail'),
]