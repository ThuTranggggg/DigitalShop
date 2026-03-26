from django.urls import path

from .views import ClothesDetailView, ClothesListCreateView, ClothesSearchView, ClothesStockAdjustView

urlpatterns = [
    path("clothes/", ClothesListCreateView.as_view(), name="clothes-list-create"),
    path("clothes/search/", ClothesSearchView.as_view(), name="clothes-search"),
    path("clothes/<int:pk>/", ClothesDetailView.as_view(), name="clothes-detail"),
    path("clothes/<int:pk>/stock-adjust/", ClothesStockAdjustView.as_view(), name="clothes-stock-adjust"),
]
