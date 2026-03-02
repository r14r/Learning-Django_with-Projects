from django.contrib import admin
from django.urls import path
from analytics_dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]