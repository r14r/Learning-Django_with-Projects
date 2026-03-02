from django.contrib import admin
from django.urls import path
from rest_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]