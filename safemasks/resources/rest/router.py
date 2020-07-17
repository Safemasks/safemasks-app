"""
"""
from rest_framework import routers

from safemasks.resources.rest.serializers import ProductViewSet, TrustedSupplierViewSet


# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()
# ROUTER.register(r"products", ProductViewSet)
ROUTER.register(r"suppliers-trusted", TrustedSupplierViewSet)
