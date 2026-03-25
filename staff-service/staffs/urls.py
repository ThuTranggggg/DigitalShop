from django.urls import path

from .views import (
    StaffLaptopCreateView,
    StaffLaptopDetailView,
    StaffLoginView,
    StaffMobileCreateView,
    StaffMobileDetailView,
    StaffProductsOverviewView,
    StaffProfileView,
)

urlpatterns = [
    path("staff/login/", StaffLoginView.as_view(), name="staff-login"),
    path("staff/profile/", StaffProfileView.as_view(), name="staff-profile"),
    path("staff/laptops/", StaffLaptopCreateView.as_view(), name="staff-laptop-create"),
    path("staff/laptops/<int:product_id>/", StaffLaptopDetailView.as_view(), name="staff-laptop-detail"),
    path("staff/mobiles/", StaffMobileCreateView.as_view(), name="staff-mobile-create"),
    path("staff/mobiles/<int:product_id>/", StaffMobileDetailView.as_view(), name="staff-mobile-detail"),
    path("staff/products/overview/", StaffProductsOverviewView.as_view(), name="staff-products-overview"),
]
