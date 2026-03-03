from django.urls import path
from . import views

app_name = 'movie_database'
urlpatterns = [
    path('',                   views.MovieListView.as_view(),   name='list'),
    path('genre/<slug:slug>/', views.MovieListView.as_view(),   name='genre'),
    path('movie/<slug:slug>/', views.MovieDetailView.as_view(), name='detail'),
]