from django.urls import path

from .views import (
    CartView,
    CartItemCreateView,
    CartItemDetailView,
    CartSummaryView,
)

urlpatterns = [
    path("customers/cart/", CartView.as_view(), name="cart"),
    path("customers/cart/items/", CartItemCreateView.as_view(), name="cart-item-create"),
    path("customers/cart/items/<int:item_id>/", CartItemDetailView.as_view(), name="cart-item-detail"),
    path("customers/cart/summary/", CartSummaryView.as_view(), name="cart-summary"),
]
