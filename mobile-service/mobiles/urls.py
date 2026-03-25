from django.urls import path

from .views import MobileDetailView, MobileListCreateView, MobileSearchView

urlpatterns = [
    path("mobiles/", MobileListCreateView.as_view(), name="mobile-list-create"),
    path("mobiles/search/", MobileSearchView.as_view(), name="mobile-search"),
    path("mobiles/<int:pk>/", MobileDetailView.as_view(), name="mobile-detail"),
]
