"""Utility module of the main app
"""
from typing import Dict

from os import environ

from django.core.exceptions import ImproperlyConfigured

BACKENDS = {
    "sqlite": {"engine": "django.db.backends.sqlite3", "mandatory_keys": set(["NAME"])},
    "pgsql": {
        "engine": "django.db.backends.postgresql",
        "mandatory_keys": set(["NAME", "USER", "PASSWORD", "HOST", "PORT"]),
    },
    "mysql": {
        "engine": "django.db.backends.mysql",
        "mandatory_keys": set(["NAME", "USER", "PASSWORD", "HOST", "PORT"]),
    },
}


def parse_db_from_environ() -> Dict[str, str]:
    """Parses SAFEMASKS_DB variables from environment to establish connection to the DB
    """
    backend = environ.get("SAFEMASKS_DB_BACKEND", None)
    if not backend:
        raise ImproperlyConfigured("You must specify a DB backend to run the app.")

    if not backend in BACKENDS:
        raise ImproperlyConfigured(
            "Unknown DB backend `{backend}`. Must be one out of {keys}".format(
                backend=backend, keys=BACKENDS.keys()
            )
        )

    db_environ_keys = {
        key.replace("SAFEMASKS_DB_", ""): environ.get(key)
        for key in environ
        if key.startswith("SAFEMASKS_DB_")
    }

    missing_keys = BACKENDS[backend]["mandatory_keys"] - db_environ_keys.keys()
    if missing_keys:
        raise ImproperlyConfigured(
            "To use the `{backend}` DB backend, you have to specify {keys}".format(
                backend=backend, keys=["SAFEMASKS_DB_" + key for key in missing_keys]
            )
        )

    return {"ENGINE": BACKENDS[backend]["engine"], **db_environ_keys}
