"""This file implements the tables storing information about suppliers

"""
from typing import List

from django.db import models
from django.contrib.auth.models import User

from django.core.validators import URLValidator, EmailValidator
from django.core.exceptions import ValidationError

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
        help_text="Name of the supplier.", unique=True, max_length=512
    )
    addresses = models.TextField(
        help_text="Addresses of the supplier."
        " Comma seperated list of URLs or E-Mail addresses.",
        null=True,
        blank=True,
    )
    company_type = models.CharField(
        choices=[("sup", "Supplier"), ("man", "Manufacturer")],
        max_length=3,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        """Name of the supplier"""
        return self.name

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
        help_text="Name of the product",
    )
    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
        help_text="Who supplied this product?",
        related_name="products",
    )
    certificate = models.CharField(
        null=True, blank=True, help_text="Certificate of the supplier", max_length=128
    )
    trustworthy = models.BooleanField(
        blank=False,
        null=False,
        help_text="Is the supplier trustworthy and fulfills standards?"
        " Aggregates reviews.",
    )
    last_update = models.DateTimeField(help_text="When was this entry last updated?")

    class Meta:
        unique_together = ["name", "supplier"]

    def __str__(self) -> str:
        """Name of the product"""
        return "{product}, {supplier}".format(product=self.name, supplier=self.supplier)

    @property
    def n_reviews(self) -> str:
        """Returns number of reviews
        """
        return self.appears_in_reviews.count()


class ProductReview(models.Model):
    """Table represents a review for a given product.

    This allows to track multiple sources.
    """

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        help_text="What was the product?",
        related_name="appears_in_reviews",
    )
    source = models.TextField(help_text="How was this information obtained?")
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text="Who submitted this information?",
        related_name="reviews",
    )
    last_update = models.DateTimeField(help_text="When was the review last updated?")
    trustworthy = models.BooleanField(
        blank=False,
        null=False,
        help_text="Is the product trustworthy and fulfills standards?",
    )
    comment = models.TextField(
        null=True, blank=True, help_text="Additional information to support review."
    )

    def __str__(self) -> str:
        """Rating summary"""
        return "Rating({user}->{product}, trustworthy={trustworthy})".format(
            user=self.user, product=self.product, trustworthy=self.trustworthy
        )


class ProductDelivery(models.Model):
    """Table represents executed deliveries.

    This allows to track if suppliers met their demands.
    """

    verbose_name_plural = "Product deliveries"

    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, help_text="Which product was delivered?"
    )
    amount = models.PositiveIntegerField(help_text="How many items were delivered?")
    price_per_unit = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price per unit in Euro.",
    )
    receiver = models.CharField(max_length=512, help_text="Who obtained the delivery?",)
    delivered_in_time = models.BooleanField(
        null=True, blank=True, help_text="Was the product delivered in time?"
    )
    last_update = models.DateTimeField(help_text="When was this entry last updated?")

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
        max_length=128, help_text="Name of the resource", unique=True
    )
    address = models.URLField(help_text="Address of the resource")
    supplements = models.TextField(
        null=True, blank=True, help_text="Additional information about resource."
    )

    def __str__(self) -> str:
        """Name of the resource"""
        return self.name
