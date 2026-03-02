from django.contrib import admin
from django.urls import path
from hello_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]