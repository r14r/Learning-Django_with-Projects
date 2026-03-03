from django.urls import path
from . import views

app_name = 'social_network'
urlpatterns = [
    path('',                              views.FeedView.as_view(),        name='feed'),
    path('explore/',                      views.ExploreView.as_view(),     name='explore'),
    path('profile/<str:username>/',       views.profile_view,              name='profile'),
    path('profile/edit/',                 views.ProfileEditView.as_view(), name='profile-edit'),
    path('post/create/',                  views.PostCreateView.as_view(),  name='post-create'),
    path('post/<int:pk>/delete/',         views.PostDeleteView.as_view(),  name='post-delete'),
    path('post/<int:pk>/like/',           views.like_post,                 name='like'),
    path('post/<int:pk>/comment/',        views.add_comment,               name='comment'),
    path('follow/<str:username>/',        views.follow_view,               name='follow'),
]