"""Collects querries reused over app."""
from django.db.models import Count, Avg, Max
from django.db.models.functions import Coalesce


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
