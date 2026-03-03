from django.urls import path
from . import views

app_name = 'book_library'
urlpatterns = [
    path('',              views.BookListView.as_view(),   name='list'),
    path('<int:pk>/',     views.BookDetailView.as_view(), name='detail'),
    path('add/',          views.BookCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.BookUpdateView.as_view(), name='update'),
    path('<int:pk>/del/', views.BookDeleteView.as_view(), name='delete'),
]
