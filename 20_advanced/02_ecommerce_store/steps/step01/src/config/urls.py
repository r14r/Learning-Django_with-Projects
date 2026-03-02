from django.contrib import admin
from django.urls import path
from ecommerce_store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       views.home, name='home'),
]