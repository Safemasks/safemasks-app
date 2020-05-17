#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    if (
        "SAFEMASKS_ENVIRONMENT" not in os.environ
        or "SAFEMASKS_SECRET_KEY" not in os.environ
    ):
        raise KeyError("Could not read SAFEMASKS environment variables.")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safemasks.safemasks.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
