"""Collects querries reused over app."""
from django.db.models import Count, Avg, Max, Q
from django.db.models.functions import Coalesce

from safemasks.resources.models import Supplier


def annotate_suppliers(qs):
    return (
        qs.annotate(n_reviews_qs=Count("reviews"))
        .annotate(latest_review_qs=Max("reviews__last_update"))
        .annotate(latest_product_review_qs=Max("products__reviews__last_update"))
        .annotate(
            last_update_qs=Coalesce("latest_product_review_qs", "latest_review_qs")
        )
        .annotate(n_products_qs=Count("products"))
        .annotate(n_product_ratings_qs=Count("products__reviews"))
        .annotate(avg_rating_qs=Avg("reviews__rating"))
        .annotate(avg_product_rating_qs=Avg("products__reviews__rating"))
    )


def annotate_reviews(qs):
    return (
        qs.annotate(n_reviews_qs=Count("reviews"))
        .annotate(latest_review_qs=Max("reviews__last_update"))
        .annotate(avg_rating_qs=Avg("reviews__rating"))
    )


def trustworty_suppliers():
    """Returns all trusted suppliers.

    A supplier is trusted if either the average product or average supplier rating
    is above 0.5. If one rating is above 0.5 and the other is below 0.5, the supplier
    is not trusted.
    """
    positive_rating = Q(avg_rating_qs__isnull=False) & Q(avg_rating_qs__gte=0.5)
    positive_product_rating = Q(avg_product_rating_qs__isnull=False) & Q(
        avg_product_rating_qs__gte=0.5
    )
    negative_rating = Q(avg_rating_qs__isnull=False) & Q(avg_rating_qs__lt=-0.5)
    negative_product_rating = Q(avg_product_rating_qs__isnull=False) & Q(
        avg_product_rating_qs__lt=-0.5
    )
    return (
        annotate_suppliers(Supplier.objects.all())
        .filter(positive_rating | positive_product_rating)
        .exclude(negative_rating)
        .exclude(negative_product_rating)
    )
