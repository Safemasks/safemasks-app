"""Prepares the usage of the safemasks module
"""
import os
from django import setup as _setup


def _init():
    """Initializes the django environment for safemasks
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safemasks.safemasks.settings")
    _setup()


_init()
