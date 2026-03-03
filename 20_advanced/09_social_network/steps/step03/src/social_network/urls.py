from django.urls import path
from . import views

app_name = 'social_network'
urlpatterns = [
    path('',                        views.ExploreView.as_view(),  name='explore'),
    path('profile/<str:username>/', views.profile_view,           name='profile'),
    path('follow/<str:username>/',  views.follow_view,            name='follow'),
]