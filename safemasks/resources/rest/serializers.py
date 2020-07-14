"""Rest API serializers for resources
"""
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from safemasks.resources.models import Product, Supplier


class SupplierSerializer(ModelSerializer):
    """Serializer of companies
    """

    class Meta:
        model = Supplier
        fields = ["name", "addresses", "company_type"]


class ProductSerializer(ModelSerializer):
    """Serializer of products
    """

    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = ["name", "supplier", "certificate", "last_update"]


class ProductViewSet(ModelViewSet):  # pylint: disable=R0901
    """Serializer view for only untrustworthy products
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
