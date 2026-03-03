from django.urls import path
from . import views

app_name = 'user_auth'
urlpatterns = [
    path('',               views.DashboardView.as_view(),  name='list'),
    path('register/',      views.RegisterView.as_view(),   name='register'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='detail'),
    path('profile/edit/',  views.ProfileEditView.as_view(), name='update'),
]
