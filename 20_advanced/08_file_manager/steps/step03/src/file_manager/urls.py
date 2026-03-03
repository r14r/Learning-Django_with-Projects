from django.urls import path
from . import views

app_name = 'file_manager'
urlpatterns = [
    path('',          views.FileListView.as_view(), name='list'),
    path('upload/',   views.upload_view,            name='upload'),
]