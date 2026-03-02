from django.contrib import admin
from django.urls import path
from file_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]