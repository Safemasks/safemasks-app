"""Django admin setup for models
"""

from django.contrib.admin import register, ModelAdmin, TabularInline
from django.db.models import TextField
from django.forms import Textarea

from safemasks.resources.models import (
    Supplier,
    Product,
    ProductReview,
    SupplierReview,
    ProductDelivery,
    RemoteDatabase,
)


class SupplierReviewInline(TabularInline):
    model = SupplierReview
    extra = 0
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 40})},
    }


@register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ("name", "addresses", "company_type", "last_update")


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
        "avg_rating",
        "n_reviews",
        "avg_product_rating",
        "n_products",
        "last_update",
    )
    inlines = (ProductReviewInline,)
    list_filter = ("name",)


@register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ("product", "source", "user", "last_update", "rating")


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
