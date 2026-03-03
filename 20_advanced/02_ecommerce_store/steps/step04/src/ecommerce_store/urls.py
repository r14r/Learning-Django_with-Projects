from django.urls import path
from . import views

app_name = 'ecommerce_store'
urlpatterns = [
    path('',                         views.ProductListView.as_view(),  name='product-list'),
    path('category/<slug:slug>/',    views.ProductListView.as_view(),  name='category'),
    path('product/<slug:slug>/',     views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/',                    views.cart_view,     name='cart'),
    path('cart/add/<int:pk>/',       views.cart_add,      name='cart-add'),
    path('cart/remove/<int:pk>/',    views.cart_remove,   name='cart-remove'),
    path('checkout/',                views.checkout_view, name='checkout'),
    path('orders/',                  views.order_list,    name='order-list'),
    path('orders/<int:pk>/',         views.order_detail,  name='order-detail'),
]