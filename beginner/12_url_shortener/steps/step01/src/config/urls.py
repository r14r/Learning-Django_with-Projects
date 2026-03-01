from django.contrib import admin
from django.urls import path
from url_shortener import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]