"""
"""
from rest_framework import routers

from safemasks.resources.rest.serializers import SupplierViewSet, TrustedSupplierViewSet


# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()
ROUTER.register(r"suppliers", SupplierViewSet)
ROUTER.register(r"suppliers-trusted", TrustedSupplierViewSet)
