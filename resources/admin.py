"""Django admin setup for models
"""

from django.contrib.admin import register, ModelAdmin, TabularInline
from django.db.models import TextField
from django.forms import Textarea

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


class ProductReviewInline(TabularInline):
    model = ProductReview
    extra = 0
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 40})},
    }


@register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "supplier",
        "certificate",
        "trustworthy",
        "n_reviews",
        "last_update",
    )
    inlines = (ProductReviewInline,)


@register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ("product", "source", "user", "last_update", "trustworthy")


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
