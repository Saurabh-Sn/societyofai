from django.urls import path
from .views import HomeView, add_to_cart, OrderSummaryView, remove_item_from_cart, CheckoutView, remove_from_cart


urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<pk>/', remove_item_from_cart,
         name='remove-item-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
]