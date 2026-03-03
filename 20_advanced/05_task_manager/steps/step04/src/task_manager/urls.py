from django.urls import path
from . import views

app_name = 'task_manager'
urlpatterns = [
    path('',                                   views.TaskListView.as_view(),   name='list'),
    path('board/',                             views.board_view,               name='board'),
    path('task/<int:pk>/',                     views.TaskDetailView.as_view(), name='detail'),
    path('task/create/',                       views.TaskCreateView.as_view(), name='create'),
    path('task/<int:pk>/edit/',                views.TaskUpdateView.as_view(), name='update'),
    path('task/<int:pk>/delete/',              views.TaskDeleteView.as_view(), name='delete'),
    path('task/<int:pk>/status/<str:status>/', views.update_status,            name='update-status'),
    path('task/<int:pk>/comment/',             views.add_comment,              name='add-comment'),
]