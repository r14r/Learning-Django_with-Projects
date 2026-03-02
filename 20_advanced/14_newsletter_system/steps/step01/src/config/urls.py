from django.contrib import admin
from django.urls import path
from newsletter_system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]