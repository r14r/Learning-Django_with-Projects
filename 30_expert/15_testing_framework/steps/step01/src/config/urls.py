from django.contrib import admin
from django.urls import path
from testing_framework import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]