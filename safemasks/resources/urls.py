"""safemasks.resources URL Configuration
"""
from django.urls import path, include
from safemasks.resources.rest.router import ROUTER
from safemasks.resources.views import (
    IndexView,
    ProductDetailView,
    ProductListView,
    TrustedProductView,
    SupplierDetailView,
    SupplierListView,
)

app_name = "resources"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("products/list/", ProductListView.as_view(), name="product-list"),
    path("products/detail/", ProductDetailView.as_view(), name="product-detail"),
    path("products/trusted/", TrustedProductView.as_view(), name="product-trusted"),
    path("suppliers/list/", SupplierListView.as_view(), name="supplier-list"),
    path("suppliers/detail/", SupplierDetailView.as_view(), name="supplier-detail"),
    path("api/", include((ROUTER.urls, "resources"), namespace="api")),
]
