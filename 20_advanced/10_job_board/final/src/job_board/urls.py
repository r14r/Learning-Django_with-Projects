from django.urls import path
from . import views

app_name = 'job_board'
urlpatterns = [
    path('',                               views.JobListView.as_view(),    name='list'),
    path('job/<int:pk>/',                  views.JobDetailView.as_view(),  name='detail'),
    path('job/create/',                    views.JobCreateView.as_view(),  name='create'),
    path('job/<int:pk>/apply/',            views.apply_view,               name='apply'),
    path('dashboard/',                     views.employer_dashboard,       name='employer-dashboard'),
    path('my-applications/',              views.applicant_dashboard,       name='my-applications'),
    path('application/<int:pk>/status/<str:status>/', views.update_status, name='update-status'),
]
