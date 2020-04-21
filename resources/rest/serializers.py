"""
"""

from resources.models import Product, Supplier
from rest_framework.serializers import ModelSerializer, RelatedField
from rest_framework.viewsets import ModelViewSet


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["name", "addresses", "company_type"]


class ProductSerializer(ModelSerializer):
    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = ["name", "supplier", "certificate", "trustworthy", "last_update"]


class BlackListViewSet(ModelViewSet):
    queryset = Product.objects.filter(trustworthy=False)
    serializer_class = ProductSerializer
