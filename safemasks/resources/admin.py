"""Django admin setup for models
"""

from django.contrib.admin import register, ModelAdmin, StackedInline, SimpleListFilter
from django.db.models import TextField, Q
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from safemasks.resources.models import Supplier, Product, ProductReview, SupplierReview
from safemasks.resources.querysets import annotate_suppliers, annotate_reviews


class SupplierReviewInline(StackedInline):
    model = SupplierReview
    extra = 0
    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 40})},
    }


class RatingListFilter(SimpleListFilter):
    title = _("Rating")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return (
            ("+", _("Positive")),
            ("0", _("Neutral")),
            ("-", _("Negativ")),
        )

    def queryset(self, request, queryset):
        key = self.parameter_name
        if self.value() == "+":
            query = {f"{key}__gte": 0.5, f"{key}__isnull": False}
        elif self.value() == "0":
            query = Q(**{f"{key}__lt": 0.5}) & Q(**{f"{key}__gte": -0.5})
            query |= Q(**{f"{key}__isnull": True})
            return queryset.filter(query)
        elif self.value() == "-":
            query = {f"{key}__lt": -0.5, f"{key}__isnull": False}
        else:
            return
        return queryset.filter(**query)


class AvgProductRatingListFilter(RatingListFilter):
    parameter_name = "avg_product_rating"
    title = _("Average Product rating")

    def queryset(self, request, queryset):
        return super().queryset(request, annotate_suppliers(queryset))


class AvgRatingListFilter(RatingListFilter):
    parameter_name = "avg_rating"
    title = _("Average rating")

    def queryset(self, request, queryset):
        return super().queryset(request, annotate_reviews(queryset))


@register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = (
        "name",
        "addresses",
        "company_type",
        "date_added",
        "last_update",
        "avg_rating",
        "n_reviews",
        "n_products",
        "avg_product_rating",
        "n_product_ratings",
    )
    inlines = (SupplierReviewInline,)
    search_fields = ("name",)
    list_filter = (
        AvgRatingListFilter,
        AvgProductRatingListFilter,
    )

    def get_queryset(self, request):  # noqa: ignore=D102

        qs = super().get_queryset(request)
        return annotate_suppliers(qs)

    # below functions wrap annotations from annotate_suppliers
    def n_reviews(self, obj):
        return obj.n_reviews

    n_reviews.short_description = "# Reviews"
    n_reviews.admin_order_field = "n_reviews"

    def last_update(self, obj):
        return obj.last_update

    last_update.short_description = "Last update"
    last_update.admin_order_field = "last_update"

    def n_products(self, obj):
        return obj.n_products

    n_products.short_description = "# Products"
    n_products.admin_order_field = "n_products"

    def n_product_ratings(self, obj):
        return obj.n_product_ratings

    n_product_ratings.short_description = "# Product Ratings"
    n_product_ratings.admin_order_field = "n_product_ratings"

    def avg_rating(self, obj):
        return obj.avg_rating

    avg_rating.short_description = "AVG Rating"
    avg_rating.admin_order_field = "avg_rating"

    def avg_product_rating(self, obj):
        return obj.avg_product_rating

    avg_product_rating.short_description = "AVG Prod. Rating"
    avg_product_rating.admin_order_field = "avg_product_rating"


@register(SupplierReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ("supplier", "source", "user", "last_update", "rating")
    search_fields = ("supplier__name",)


class ProductReviewInline(StackedInline):
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
        "date_added",
        "latest_review",
        "avg_rating",
        "n_reviews",
    )
    inlines = (ProductReviewInline,)
    list_filter = ("name", AvgRatingListFilter)
    search_fields = ("supplier__name",)

    def get_queryset(self, request):  # noqa: ignore=D102

        qs = super().get_queryset(request)
        return annotate_reviews(qs)

    def n_reviews(self, obj):
        return obj.n_reviews

    n_reviews.short_description = "# Reviews"
    n_reviews.admin_order_field = "n_reviews"

    def latest_review(self, obj):
        return obj.latest_review

    latest_review.short_description = "Last update"
    latest_review.admin_order_field = "latest_review"

    def avg_rating(self, obj):
        return obj.avg_rating

    avg_rating.short_description = "AVG Rating"
    avg_rating.admin_order_field = "avg_rating"


@register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ("product", "source", "user", "last_update", "rating")
    search_fields = ("product__name", "product__supplier__name")
