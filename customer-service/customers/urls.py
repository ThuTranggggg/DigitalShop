from django.urls import path

from .views import (
    CustomerLaptopDetailView,
    CustomerLaptopListView,
    CustomerLaptopSearchView,
    CustomerLoginView,
    CustomerMobileDetailView,
    CustomerMobileListView,
    CustomerMobileSearchView,
    CustomerProfileView,
    CustomerRegisterView,
)

urlpatterns = [
    path("customers/register/", CustomerRegisterView.as_view(), name="customer-register"),
    path("customers/login/", CustomerLoginView.as_view(), name="customer-login"),
    path("customers/profile/", CustomerProfileView.as_view(), name="customer-profile"),
    path("customers/laptops/", CustomerLaptopListView.as_view(), name="customer-laptop-list"),
    path("customers/laptops/search/", CustomerLaptopSearchView.as_view(), name="customer-laptop-search"),
    path("customers/laptops/<int:product_id>/", CustomerLaptopDetailView.as_view(), name="customer-laptop-detail"),
    path("customers/mobiles/", CustomerMobileListView.as_view(), name="customer-mobile-list"),
    path("customers/mobiles/search/", CustomerMobileSearchView.as_view(), name="customer-mobile-search"),
    path("customers/mobiles/<int:product_id>/", CustomerMobileDetailView.as_view(), name="customer-mobile-detail"),
]
