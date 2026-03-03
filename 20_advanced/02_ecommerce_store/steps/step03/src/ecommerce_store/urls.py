from django.urls import path
from . import views

app_name = 'ecommerce_store'
urlpatterns = [
    path('',                          views.ProductListView.as_view(),  name='product-list'),
    path('category/<slug:slug>/',     views.ProductListView.as_view(),  name='category'),
    path('product/<slug:slug>/',      views.ProductDetailView.as_view(), name='product-detail'),
]