"""
"""
from rest_framework import routers

from safemasks.resources.rest.serializers import ProductViewSet


# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()
ROUTER.register(r"products", ProductViewSet)
