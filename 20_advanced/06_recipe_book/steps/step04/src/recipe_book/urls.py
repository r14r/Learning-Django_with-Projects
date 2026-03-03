from django.urls import path
from . import views

app_name = 'recipe_book'
urlpatterns = [
    path('',                           views.RecipeListView.as_view(),   name='list'),
    path('category/<slug:slug>/',      views.RecipeListView.as_view(),   name='category'),
    path('recipe/<slug:slug>/',        views.RecipeDetailView.as_view(), name='detail'),
    path('recipe/create/',             views.recipe_create,              name='create'),
    path('recipe/<slug:slug>/edit/',   views.recipe_edit,                name='update'),
    path('recipe/<slug:slug>/delete/', views.RecipeDeleteView.as_view(), name='delete'),
    path('my-recipes/',                views.MyRecipesView.as_view(),    name='my-recipes'),
]