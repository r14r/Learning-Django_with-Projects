from django.urls import path

from . import views

app_name = 'poll_app'
urlpatterns = [
    path('', views.PollListView.as_view(), name='list'),
    path('<int:pk>/', views.PollDetailView.as_view(), name='detail'),
    path('<int:pk>/vote/', views.VoteView.as_view(), name='vote'),
    path('create/', views.PollCreateView.as_view(), name='create'),
    path('<int:pk>/del/', views.PollDeleteView.as_view(), name='delete'),
]
