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
    parameter_name = "avg_product_rating_qs"
    title = _("Average Product rating")

    def queryset(self, request, queryset):
        return super().queryset(request, annotate_suppliers(queryset))


class AvgRatingListFilter(RatingListFilter):
    parameter_name = "avg_rating_qs"
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
        "last_update_qs",
        "avg_rating_qs",
        "n_reviews_qs",
        "n_products_qs",
        "avg_product_rating_qs",
        "n_product_ratings_qs",
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
    def n_reviews_qs(self, obj):
        return obj.n_reviews_qs

    n_reviews_qs.short_description = "# Reviews"
    n_reviews_qs.admin_order_field = "n_reviews_qs"

    def last_update_qs(self, obj):
        return obj.last_update_qs

    last_update_qs.short_description = "Last update"
    last_update_qs.admin_order_field = "last_update_qs"

    def n_products_qs(self, obj):
        return obj.n_products_qs

    n_products_qs.short_description = "# Products"
    n_products_qs.admin_order_field = "n_products_qs"

    def n_product_ratings_qs(self, obj):
        return obj.n_product_ratings_qs

    n_product_ratings_qs.short_description = "# Product Ratings"
    n_product_ratings_qs.admin_order_field = "n_product_ratings_qs"

    def avg_rating_qs(self, obj):
        return obj.avg_rating_qs

    avg_rating_qs.short_description = "AVG Rating"
    avg_rating_qs.admin_order_field = "avg_rating_qs"

    def avg_product_rating_qs(self, obj):
        return obj.avg_product_rating_qs

    avg_product_rating_qs.short_description = "AVG Prod. Rating"
    avg_product_rating_qs.admin_order_field = "avg_product_rating_qs"


@register(SupplierReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ("supplier", "source", "user", "last_update", "rating")


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
        "avg_rating",
        "n_reviews",
        "last_update",
    )
    inlines = (ProductReviewInline,)
    list_filter = ("name",)


@register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    list_display = ("product", "source", "user", "last_update", "rating")
