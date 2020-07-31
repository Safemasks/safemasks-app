"""This file implements the tables storing information about suppliers
"""
from typing import List, Optional

from django.db import models
from django.contrib.auth.models import User

from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.template.defaultfilters import truncatechars
from django.utils import timezone

from django.utils.translation import gettext_lazy as _


URL_VALIDATOR = URLValidator()
EMAIL_VALIDATOR = EmailValidator()


def is_email_or_url(string: str) -> bool:
    """Checks if string is either an email or url.
    """
    out = False
    try:
        URL_VALIDATOR(string)
        out = True
    except ValidationError:
        pass

    try:
        URL_VALIDATOR(string)
        out = True
    except ValidationError:
        pass

    return out


class Supplier(models.Model):
    """Suppliers represented in the safemasks tables
    """

    name = models.CharField(
        help_text=_("Name of the supplier."), unique=True, max_length=512
    )
    addresses = models.TextField(
        help_text=_(
            "Addresses of the supplier."
            " Comma seperated list of URLs or E-Mail addresses."
        ),
        null=True,
        blank=True,
    )
    company_type = models.CharField(
        choices=[("sup", _("Supplier")), ("man", _("Manufacturer"))],
        max_length=3,
        blank=True,
        null=True,
    )
    comment = models.TextField(
        null=True,
        blank=True,
        help_text=_("Additional information which help informing about this supplier."),
    )
    references = models.TextField(
        null=True,
        blank=True,
        help_text=_("Links and references to crossh-check this supplier."),
    )
    date_added = models.DateTimeField(
        help_text=_("When was this supplier added to the safemasks portal?"),
        default=timezone.now,
    )

    @property
    def short_name(self):
        """Abbrevieates name to 100 chars"""
        return truncatechars(self.name, 40)

    def __str__(self) -> str:
        """Name of the supplier"""
        return self.short_name

    def address_list(self) -> List[str]:
        """Returns the addresses as a list of urls or emails.
        """
        return [address.strip() for address in self.addresses.split(",")]

    def clean(self):
        """Checks if input for addresses are either emails or urls in correct format.
        """
        if self.addresses:
            addresses = []
            for address in self.addresses.split(","):
                address = address.strip()
                if not is_email_or_url(address):
                    raise ValidationError(
                        "The address '{address}' is neither an URL nor E-mail.".format(
                            address=address
                        )
                    )
                addresses.append(address)
            self.addresses = ", ".join(addresses)


PRODUCT_NAME_CHOICES = {
    "Mask": "mask",
    "Ventilator": "vent",
    "Sanitizer": "sani",
    "Desinfektionsmittel": "sani",
    "Beatmungsgerät": "vent",
}
_PRODUCT_NAME_CHOICES = {
    "Mask": "mask",
    "Ventilator": "vent",
    "Sanitizer": "sani",
}


class Product(models.Model):
    """Products represented in the safemasks tables
    """

    name = models.CharField(
        choices=list(zip(_PRODUCT_NAME_CHOICES.values(), _PRODUCT_NAME_CHOICES.keys())),
        max_length=4,
        help_text=_("Name of the product"),
    )
    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
        help_text=_("Who supplied this product?"),
        related_name="products",
    )
    certificate = models.CharField(
        null=True, blank=True, help_text=_("Certificate of the product"), max_length=128
    )
    comment = models.TextField(
        null=True,
        blank=True,
        help_text=_("Additional information which help informing about this product."),
    )
    references = models.TextField(
        null=True,
        blank=True,
        help_text=_("Links and references to crossh-check this product."),
    )
    date_added = models.DateTimeField(
        help_text=_("When was this product added to the safemasks portal?"),
        default=timezone.now,
    )

    class Meta:
        unique_together = ["name", "supplier"]

    def __str__(self) -> str:
        """Name of the product"""
        return "{product}, {supplier}".format(product=self.name, supplier=self.supplier)

    def get_n_reviews(self) -> int:
        """Returns number of reviews
        """
        return self.reviews.count()

    def get_avg_rating(self) -> Optional[float]:
        ratings = self.reviews.values_list("rating", flat=True)
        return sum(ratings) / len(ratings) if ratings else None

    def get_last_update(self):
        last_update = None
        if self.reviews.exists():
            last_update = self.reviews.latest("last_update").last_update

        return last_update


RATING_CHOICES = [(-1, _("Negativ")), (0, _("Neutral")), (1, _("Positiv"))]


class Review(models.Model):
    """
    """

    source = models.TextField(help_text=_("How was this information obtained?"))
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text=_("Who submitted this information?"),
    )
    last_update = models.DateTimeField(
        help_text=_("When was the review last updated?"), default=timezone.now
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        blank=False,
        null=False,
        help_text=_(
            "Is the entry trustworthy? Ranges from -1 (negativ) to +1 (positiv)."
        ),
    )
    comment = models.TextField(
        null=True, blank=True, help_text=_("Additional information to support review.")
    )

    class Meta:
        abstract = True


class ProductReview(Review):
    """Table represents a review for a given product.

    This allows to track multiple sources.
    """

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        help_text=_("What was the product?"),
        related_name="reviews",
    )

    def __str__(self) -> str:
        """Rating summary"""
        return "Rating({user}->{product}, rating={rating})".format(
            user=self.user, product=self.product, rating=self.rating
        )


class SupplierReview(Review):
    """Table represents a review for a given product.

    This allows to track multiple sources.
    """

    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
        help_text=_("Who is the supplier?"),
        related_name="reviews",
    )

    def __str__(self) -> str:
        """Rating summary"""
        return "Rating({user}->{supplier}, rating={rating})".format(
            user=self.user, supplier=self.supplier, rating=self.rating
        )


class ProductDelivery(models.Model):
    """Table represents executed deliveries.

    This allows to track if suppliers met their demands.
    """

    verbose_name_plural = _("Product deliveries")

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        help_text=_("Which product was delivered?"),
    )
    amount = models.PositiveIntegerField(help_text=_("How many items were delivered?"))
    price_per_unit = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Price per unit in Euro."),
    )
    receiver = models.CharField(
        max_length=512, help_text=_("Who obtained the delivery?"),
    )
    delivered_in_time = models.BooleanField(
        null=True, blank=True, help_text=_("Was the product delivered in time?")
    )
    last_update = models.DateTimeField(help_text=_("When was this entry last updated?"))

    def __str__(self) -> str:
        """Name of the list"""
        return ("Delivery({product}->{receiver}, in_time={delivered_in_time})").format(
            product=self.product,
            receiver=self.receiver,
            delivered_in_time=self.delivered_in_time,
        )


class RemoteDatabase(models.Model):
    """Table represents remote resources to extract information from.
    """

    name = models.CharField(
        max_length=128, help_text=_("Name of the resource"), unique=True
    )
    address = models.URLField(help_text=_("Address of the resource"))
    supplements = models.TextField(
        null=True, blank=True, help_text=_("Additional information about resource.")
    )

    def __str__(self) -> str:
        """Name of the resource"""
        return self.name
