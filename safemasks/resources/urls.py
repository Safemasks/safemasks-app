"""safemasks.resources URL Configuration
"""
from django.urls import path, include
from safemasks.resources.rest.router import ROUTER
from safemasks.resources.views import (
    IndexView,
    ProductDetailView,
    ProductListView,
    TrustedSuppliersView,
    SupplierDetailView,
    SupplierListView,
)

app_name = "resources"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # path("products/", ProductListView.as_view(), name="product-list"),
    path(
        "products/details/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
    path(
        "suppliers/trusted/", TrustedSuppliersView.as_view(), name="suppliers-trusted"
    ),
    path("suppliers/", SupplierListView.as_view(), name="supplier-list"),
    path(
        "suppliers/details/<int:pk>/",
        SupplierDetailView.as_view(),
        name="supplier-detail",
    ),
    path("api/", include((ROUTER.urls, "resources"), namespace="api")),
]
