from django.urls import path
from . import views

app_name = 'task_manager'
urlpatterns = [
    path('',              views.TaskListView.as_view(),   name='list'),
    path('board/',        views.board_view,               name='board'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
]