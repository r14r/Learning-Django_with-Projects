from django.urls import path
from . import views

app_name = 'blog_with_comments'
urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('tag/<slug:slug>/', views.PostListView.as_view(), name='tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail, name='detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
]
