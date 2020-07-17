"""Script for adding default data blacklist data from xlsx file
"""
from typing import Tuple, Dict, Any

from logging import getLogger

from datetime import datetime
from pytz import timezone

from xlrd import open_workbook, xldate_as_tuple
from pandas import read_excel, isna

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from safemasks.resources.models import (
    Supplier,
    Product,
    ProductReview,
    PRODUCT_NAME_CHOICES,
)

TZ = timezone("Europe/Berlin")

LOGGER = getLogger("safemasks")


class Command(BaseCommand):
    """Script for parsing xlsx blacklist data to db
    """

    help = "Script for parsing xlsx blacklist data to db"

    wl_col_map = {
        "Name of the supply": "supplier:name",
        "address": "supplier:addresses",
        "Product Description": "product:name",
        "Types of Companies": "supplier:company_type",
        "source of information": "productreview:source",
        "Column1": "productreview:comment",
    }
    rating = -1

    def add_arguments(self, parser):
        parser.add_argument(
            "suppliers_file", type=str, help="location of Suppliers.xlsx file."
        )

    def handle(self, *args, **options):
        """Parses specified excel file and populates data

        Updates supplier and product tables if they exist. Else creates them.
        Todo:
            For now, the logic of the code always creates new reviews because
            no date logic is implemented.
            For this reason it only populates reviews if the review table is empty.
        """

        book = open_workbook(options["suppliers_file"])
        date_spreadsheet = book.sheet_by_index(0).cell_value(1, 1)
        date_spreadsheet = datetime(
            *xldate_as_tuple(date_spreadsheet, book.datemode), tzinfo=TZ
        )

        df = (
            read_excel(options["suppliers_file"], sheet_name="Blacklist", skiprows=3)
            .rename(columns=self.wl_col_map)
            .dropna(how="all")
        )

        user, _ = User.objects.get_or_create(username="admin")

        for _, entry in df.iterrows():

            try:
                if isna(entry.get("supplier:name")):
                    continue

                supplier, _ = self.update_or_create_supplier(
                    date_added=date_spreadsheet, **entry
                )

                if isna(entry.get("product:name")):
                    continue

                product, _ = self.update_or_create_product(
                    supplier=supplier, date_added=date_spreadsheet, **entry
                )

                self.update_or_create_review(
                    product=product, last_update=date_spreadsheet, user=user, **entry
                )

            except Exception as e:  # pylint: disable=W0703
                LOGGER.error(
                    "\nFailed to parse entry %s", entry.to_dict(),
                )
                LOGGER.exception(e)

    @staticmethod
    def prep_db_entry(table_name: str, **kwargs) -> Dict[str, Any]:
        """Flattens and selects dictionary entries based on table_name

        Picks entries which start with `table_name:key` or `key` and neglects others.
        Casts NaNs to Nones.
        """
        data = {}
        for key, val in kwargs.items():
            if ":" not in key:
                kkey = key
            elif table_name == key.split(":")[0]:
                kkey = key.split(":")[1]
            else:
                kkey = None

            if kkey is not None:
                data[kkey] = None if isna(val) else val

        return data

    def update_or_create_supplier(self, **kwargs) -> Tuple[Supplier, bool]:
        """Creates supplier from meta information if not updates existing

        Filter on name field
        """
        unique_fields = ["name"]

        data = self.prep_db_entry("supplier", **kwargs)
        unique_data = {key: data.pop(key) for key in unique_fields}
        supplier = Supplier.objects.filter(**unique_data).first()
        if not supplier:
            supplier = Supplier.objects.create(**unique_data, **data)
            created = True
        else:
            for key, val in data.items():
                setattr(supplier, key, val)
            supplier.save()
            created = False

        return supplier, created

    def update_or_create_product(self, **kwargs) -> Tuple[Product, bool]:
        """Creates product from meta information if not updates existing

        Filter on name and supplier field
        """
        unique_fields = ["name", "supplier"]

        data = self.prep_db_entry("product", **kwargs)
        data["name"] = PRODUCT_NAME_CHOICES[data.get("name")]
        unique_data = {key: data.pop(key) for key in unique_fields}
        product = Product.objects.filter(**unique_data).first()
        if not product:
            product = Product.objects.create(**unique_data, **data)
            created = True
        else:
            for key, val in data.items():
                setattr(product, key, val)
            product.save()
            created = True

        return product, created

    def update_or_create_review(self, **kwargs) -> Tuple[Product, bool]:
        """Creates product review from meta information if not updates existing

        Filter on name and supplier field
        """
        data = self.prep_db_entry("productreview", rating=self.rating, **kwargs)
        data["source"] = data["source"] or "No source"
        return ProductReview.objects.get_or_create(**data)
