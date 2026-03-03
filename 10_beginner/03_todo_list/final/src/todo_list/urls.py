from django.urls import path
from . import views

app_name = 'todo_list'
urlpatterns = [
    path('',               views.TodoListView.as_view(),   name='list'),
    path('<int:pk>/',      views.TodoDetailView.as_view(), name='detail'),
    path('create/',        views.TodoCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TodoUpdateView.as_view(), name='update'),
    path('<int:pk>/del/',  views.TodoDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle/', views.toggle_done,            name='toggle'),
]
