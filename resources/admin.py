"""Django admin setup for models
"""

from django.contrib.admin import register, ModelAdmin

from resources.models import (
    Supplier,
    SupplierList,
    SupplierReview,
    Product,
    ProductDelivery,
    RemoteDatabase,
)


@register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name",)


@register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ("name", "addresses", "company_type", "trustworty")


@register(SupplierReview)
class SupplierReviewAdmin(ModelAdmin):
    list_display = ("supplier", "source", "user", "date_added", "trustworty")


@register(SupplierList)
class SupplierListAdmin(ModelAdmin):
    list_display = ("name",)


@register(ProductDelivery)
class ProductDelivery(ModelAdmin):
    list_display = (
        "product",
        "receiver",
        "amount",
        "date_send",
        "date_received",
    )


@register(RemoteDatabase)
class RemoteDataBaseAdmin(ModelAdmin):
    list_display = (
        "name",
        "address",
        "supplements",
    )
