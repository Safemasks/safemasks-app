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


class Product(models.Model):
    """Products represented in the safemasks tables
    """

    name = models.CharField(
        help_text="Name of the product", unique=True, max_length=128
    )


class Supplier(models.Model):
    """Suppliers represented in the safemasks tables
    """

    name = models.TextField(help_text="Name of the supplier.", unique=True)
    addresses = models.TextField(
        help_text="Addresses of the supplier."
        " Comma seperated list of URLs or E-Mail addresses.",
        null=True,
        blank=True,
    )
    products = models.ManyToManyField(to=Product, related_name="suppliers",)
    company_type = models.CharField(
        choices=[("sup", "Supplier"), ("man", "Manufacturer")], max_length=3
    )
    # ToDo: is this a property of the product & supplier combined?
    certificate = models.CharField(
        null=True, help_text="Certificate of the supplier", max_length=128
    )

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
                        "The '{address}' is neither an URL nor E-mail.".format(
                            address=address
                        )
                    )
                addresses.append(addresses)
            self.addresses = ", ".join(addresses)


class SupplierReview(models.Model):
    """Table represents a review for a given supplier.

    This allows to track multiple sources.
    """

    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
        help_text="Who is the supplier?",
        related_name="appears_in_reviews",
    )
    trustworty = models.BooleanField(
        blank=False,
        null=False,
        help_text="Is the supplier trustworty and fulfills standards?",
    )
    source = models.TextField(help_text="How was this information obtained?")
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text="Who submitted this information?",
        related_name="reviews",
    )
    date_added = models.DateTimeField(
        auto_now=True, help_text="When was the review added?"
    )


class SupplierList(models.Model):
    """Table represents a list of suppliers.

    This allows grouping suppliers into different categories
    (like white list or black list).
    """

    name = models.CharField(max_length=128, help_text="Name of the list.", unique=True)
    suppliers = models.ManyToManyField(
        to=Supplier,
        help_text="Suppliers contained in the list.",
        related_name="appears_in_lists",
    )


class Delivery(models.Model):
    """Table represents executed deliveries.

    This allows to track if suppliers met their demands.
    """

    supplier = models.ForeignKey(
        to=Supplier,
        on_delete=models.CASCADE,
        related_name="appears_in_deliveries",
        help_text="Who send out the delivery?",
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, help_text="Which product was delivered?"
    )
    amount = models.PositiveIntegerField(help_text="How many items were delivered?")
    price_rating = models.IntegerField(
        choices=[(1, "low price"), (2, "fair price"), (3, "high price")],
        help_text="Was the price reasonable?",
    )
    receiver = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        help_text="Who obtained the delivery?",
        related_name="obtained_deliveries",
    )
    date_added = models.DateTimeField(
        auto_now=True, help_text="When was the review added?"
    )


class RemoteDataBase(models.Model):
    """Table represents remote resources to extract information from.
    """

    name = models.CharField(
        max_length=128, help_text="Name of the resource", unique=True
    )
    address = models.URLField(help_text="Address of the resource")
    products = models.ManyToManyField(
        to=Product,
        help_text="About which information does this resource inform?",
        related_name="appears_in_databases",
    )
    supplements = models.TextField(
        null=True, blank=True, help_text="Additional information about resource."
    )
