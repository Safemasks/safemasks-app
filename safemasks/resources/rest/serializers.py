"""Rest API serializers for resources
"""
from django.db.models import Avg, Q

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from safemasks.resources.models import Product, Supplier
from safemasks.resources.querysets import trustworty_suppliers


class TrustedSupplierSerializer(ModelSerializer):
    """Serializer of companies
    """

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "last_update",
        ]


class SupplierSerializer(ModelSerializer):
    """Serializer of companies
    """

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "last_update",
        ]


class ProductSerializer(ModelSerializer):
    """Serializer of products
    """

    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "supplier", "certificate", "last_update", "references"]


class TrustedSupplierViewSet(ModelViewSet):  # pylint: disable=R0901
    """Serializer view for only trustworty suppliers

    Trustworty is defined by avg rating of
    """

    permission_classes = []
    queryset = trustworty_suppliers()
    serializer_class = TrustedSupplierSerializer


class ProductViewSet(ModelViewSet):  # pylint: disable=R0901
    """Serializer view for only untrustworthy products
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
