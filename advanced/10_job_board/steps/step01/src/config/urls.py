from django.contrib import admin
from django.urls import path
from job_board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]