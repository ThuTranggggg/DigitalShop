from django.urls import path

from .views import (
    CheckoutView,
    CustomerClothesDetailView,
    CustomerClothesListView,
    CustomerClothesSearchView,
    CustomerLaptopDetailView,
    CustomerLaptopListView,
    CustomerLaptopSearchView,
    CustomerLoginView,
    CustomerProfileView,
    CustomerRegisterView,
    InvoiceCancelView,
    InvoiceDetailView,
    InvoiceListView,
)

urlpatterns = [
    path("customers/register/", CustomerRegisterView.as_view(), name="customer-register"),
    path("customers/login/", CustomerLoginView.as_view(), name="customer-login"),
    path("customers/profile/", CustomerProfileView.as_view(), name="customer-profile"),
    path("customers/laptops/", CustomerLaptopListView.as_view(), name="customer-laptop-list"),
    path("customers/laptops/search/", CustomerLaptopSearchView.as_view(), name="customer-laptop-search"),
    path("customers/laptops/<int:product_id>/", CustomerLaptopDetailView.as_view(), name="customer-laptop-detail"),
    path("customers/clothes/", CustomerClothesListView.as_view(), name="customer-clothes-list"),
    path("customers/clothes/search/", CustomerClothesSearchView.as_view(), name="customer-clothes-search"),
    path("customers/clothes/<int:product_id>/", CustomerClothesDetailView.as_view(), name="customer-clothes-detail"),
    path("customers/checkout/", CheckoutView.as_view(), name="customer-checkout"),
    path("customers/invoices/", InvoiceListView.as_view(), name="invoice-list"),
    path("customers/invoices/<int:invoice_id>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("customers/invoices/<int:invoice_id>/cancel/", InvoiceCancelView.as_view(), name="invoice-cancel"),
]
