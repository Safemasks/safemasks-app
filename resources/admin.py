"""Django admin setup for models
"""

from django.contrib.admin import register, ModelAdmin

from resources.models import (
    Supplier,
    Product,
    ProductReview,
    ProductDelivery,
    RemoteDatabase,
)


@register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ("name", "addresses", "company_type")


@register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "supplier", "certificate", "trustworthy", "last_update")


@register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ("product", "source", "user", "date_added", "trustworthy")


@register(ProductDelivery)
class ProductDeliveryAdmin(ModelAdmin):
    list_display = (
        "product",
        "receiver",
        "amount",
        "price_per_unit",
        "delivered_in_time",
    )


@register(RemoteDatabase)
class RemoteDataBaseAdmin(ModelAdmin):
    list_display = (
        "name",
        "address",
        "supplements",
    )
