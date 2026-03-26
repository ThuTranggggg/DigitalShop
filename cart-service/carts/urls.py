from django.urls import path

from .views import CartByCustomerView, CartClearView, CartEnsureView, CartItemCreateView, CartItemDetailView, CartSummaryView

urlpatterns = [
    path("carts/", CartEnsureView.as_view(), name="cart-ensure"),
    path("carts/customer/<int:customer_id>/", CartByCustomerView.as_view(), name="cart-by-customer"),
    path("carts/customer/<int:customer_id>/summary/", CartSummaryView.as_view(), name="cart-summary"),
    path("carts/customer/<int:customer_id>/items/", CartItemCreateView.as_view(), name="cart-item-create"),
    path("carts/customer/<int:customer_id>/items/<int:item_id>/", CartItemDetailView.as_view(), name="cart-item-detail"),
    path("carts/customer/<int:customer_id>/clear/", CartClearView.as_view(), name="cart-clear"),
]
