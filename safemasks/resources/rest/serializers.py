"""Rest API serializers for resources
"""
from django.db.models import Q

from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    IntegerField,
    FloatField,
)
from rest_framework.viewsets import ReadOnlyModelViewSet

from safemasks.resources.models import Product, Supplier
from safemasks.resources.querysets import trustworty_suppliers, annotate_suppliers


class TrustedSupplierSerializer(ModelSerializer):
    """Serializer of suppliers with limited data.
    """

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "date_added",
        ]


class SupplierSerializer(ModelSerializer):
    """Serializer of supliers with all available data.
    """

    last_update = DateTimeField()
    n_products = IntegerField()
    n_reviews = IntegerField()
    avg_rating = FloatField()
    n_product_ratings = IntegerField()
    avg_product_rating = FloatField()

    class Meta:
        model = Supplier
        fields = [
            "id",
            "name",
            "addresses",
            "company_type",
            "comment",
            "references",
            "date_added",
            "last_update",
            "n_products",
            "n_reviews",
            "avg_rating",
            "n_product_ratings",
            "avg_product_rating",
        ]


class ProductSerializer(ModelSerializer):
    """Serializer of products
    """

    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "supplier", "certificate", "last_update", "references"]


class TrustedSupplierViewSet(ReadOnlyModelViewSet):  # pylint: disable=R0901
    """List of all trusted suppliers.
    """

    permission_classes = []
    queryset = trustworty_suppliers()
    serializer_class = TrustedSupplierSerializer


class SupplierViewSet(ReadOnlyModelViewSet):  # pylint: disable=R0901
    """List of all suppliers.
    """

    queryset = annotate_suppliers(Supplier.objects.all()).exclude(
        Q(n_reviews=0) & Q(n_product_ratings=0)
    )
    serializer_class = SupplierSerializer


class ProductViewSet(ReadOnlyModelViewSet):  # pylint: disable=R0901
    """Serializer view for only untrustworthy products
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
