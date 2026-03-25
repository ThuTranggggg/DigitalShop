from django.urls import path

from .views import LaptopDetailView, LaptopListCreateView, LaptopSearchView

urlpatterns = [
    path("laptops/", LaptopListCreateView.as_view(), name="laptop-list-create"),
    path("laptops/search/", LaptopSearchView.as_view(), name="laptop-search"),
    path("laptops/<int:pk>/", LaptopDetailView.as_view(), name="laptop-detail"),
]
