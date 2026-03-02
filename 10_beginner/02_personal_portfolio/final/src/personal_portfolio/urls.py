from django.urls import path
from . import views

app_name = 'personal_portfolio'
urlpatterns = [
    path('',               views.ProjectListView.as_view(),   name='list'),
    path('<int:pk>/',      views.ProjectDetailView.as_view(), name='detail'),
    path('create/',        views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='update'),
    path('<int:pk>/del/',  views.ProjectDeleteView.as_view(), name='delete'),
]
