"""Collects querries reused over app."""
from django.db.models import Count, Avg, Max, Q
from django.db.models.functions import Coalesce

from safemasks.resources.models import Supplier


def annotate_suppliers(qs):
    return (
        qs.annotate(n_reviews=Count("reviews"))
        .annotate(latest_review=Max("reviews__last_update"))
        .annotate(latest_product_review=Max("products__reviews__last_update"))
        .annotate(last_update=Coalesce("latest_product_review", "latest_review"))
        .annotate(n_products=Count("products"))
        .annotate(n_product_ratings=Count("products__reviews"))
        .annotate(avg_rating=Avg("reviews__rating"))
        .annotate(avg_product_rating=Avg("products__reviews__rating"))
    )


def annotate_reviews(qs):
    return (
        qs.annotate(n_reviews=Count("reviews"))
        .annotate(latest_review=Max("reviews__last_update"))
        .annotate(avg_rating=Avg("reviews__rating"))
    )


def trustworty_suppliers():
    """Returns all trusted suppliers.

    A supplier is trusted if either the average product or average supplier rating
    is above 0.5. If one rating is above 0.5 and the other is below 0.5, the supplier
    is not trusted.
    """
    positive_rating = Q(avg_rating__isnull=False) & Q(avg_rating__gte=0.5)
    positive_product_rating = Q(avg_product_rating__isnull=False) & Q(
        avg_product_rating__gte=0.5
    )
    negative_rating = Q(avg_rating__isnull=False) & Q(avg_rating__lt=-0.5)
    negative_product_rating = Q(avg_product_rating__isnull=False) & Q(
        avg_product_rating__lt=-0.5
    )
    return (
        annotate_suppliers(Supplier.objects.all())
        .filter(positive_rating | positive_product_rating)
        .exclude(negative_rating)
        .exclude(negative_product_rating)
    )
