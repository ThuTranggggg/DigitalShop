from django.urls import path

from .views import (
    StaffClothesCreateView,
    StaffClothesDetailView,
    StaffDashboardView,
    StaffInventoryImportView,
    StaffLaptopCreateView,
    StaffLaptopDetailView,
    StaffLoginView,
    StaffProductsOverviewView,
    StaffProfileView,
)

urlpatterns = [
    path("staff/login/", StaffLoginView.as_view(), name="staff-login"),
    path("staff/profile/", StaffProfileView.as_view(), name="staff-profile"),
    path("staff/dashboard/", StaffDashboardView.as_view(), name="staff-dashboard"),
    path("staff/laptops/", StaffLaptopCreateView.as_view(), name="staff-laptop-create"),
    path("staff/laptops/<int:product_id>/", StaffLaptopDetailView.as_view(), name="staff-laptop-detail"),
    path("staff/clothes/", StaffClothesCreateView.as_view(), name="staff-clothes-create"),
    path("staff/clothes/<int:product_id>/", StaffClothesDetailView.as_view(), name="staff-clothes-detail"),
    path("staff/imports/", StaffInventoryImportView.as_view(), name="staff-imports"),
    path("staff/products/overview/", StaffProductsOverviewView.as_view(), name="staff-products-overview"),
]
