from django.urls import path
from . import views

app_name = 'newsletter_system'
urlpatterns = [
    path('subscribe/',               views.subscribe_view,  name='subscribe'),
    path('confirm/<uuid:token>/',    views.confirm_view,    name='confirm'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe_view, name='unsubscribe'),
]