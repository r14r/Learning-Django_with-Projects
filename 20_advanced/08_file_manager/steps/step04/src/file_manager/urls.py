from django.urls import path
from . import views

app_name = 'file_manager'
urlpatterns = [
    path('',                   views.FileListView.as_view(),     name='list'),
    path('folder/<int:pk>/',   views.FolderView.as_view(),       name='folder'),
    path('folder/create/',     views.FolderCreateView.as_view(), name='folder-create'),
    path('upload/',            views.upload_view,                name='upload'),
    path('download/<int:pk>/', views.download_view,              name='download'),
    path('delete/<int:pk>/',   views.delete_file,                name='delete'),
]