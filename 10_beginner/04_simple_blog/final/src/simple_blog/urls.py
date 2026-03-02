from django.urls import path
from . import views

app_name = 'simple_blog'
urlpatterns = [
    path('',                   views.PostListView.as_view(),   name='list'),
    path('create/',             views.PostCreateView.as_view(), name='create'),
    path('<slug:slug>/',        views.PostDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/',   views.PostUpdateView.as_view(), name='update'),
    path('<slug:slug>/del/',    views.PostDeleteView.as_view(), name='delete'),
]
