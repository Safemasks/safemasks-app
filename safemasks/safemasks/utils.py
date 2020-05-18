"""Utility module of the main app
"""
from typing import Dict

from os import environ

from django.core.exceptions import ImproperlyConfigured

DB_BACKENDS = {
    "sqlite": {"engine": "django.db.backends.sqlite3", "mandatory_keys": set(["NAME"])},
    "psql": {
        "engine": "django.db.backends.postgresql",
        "mandatory_keys": set(["NAME", "USER", "PASSWORD", "HOST", "PORT"]),
    },
    "mysql": {
        "engine": "django.db.backends.mysql",
        "mandatory_keys": set(["NAME", "USER", "PASSWORD", "HOST", "PORT"]),
    },
}

EMAIL_BACKENDS = {
    "smtp": {
        "backend": "django.core.mail.backends.smtp.EmailBackend",
        "mandatory_keys": set(
            [
                "EMAIL_HOST",
                "EMAIL_HOST_USER",
                "EMAIL_HOST_PASSWORD",
                "EMAIL_USE_SSL",
                "EMAIL_PORT",
            ]
        ),
    },
    "console": {"backend": "backends.smtp.EmailBackend", "mandatory_keys": set([])},
}


def parse_db_from_environ() -> Dict[str, str]:
    """Parses SAFEMASKS_DB variables from environment to establish connection to the DB
    """
    backend = environ.get("SAFEMASKS_DB_BACKEND", None)
    if not backend:
        raise ImproperlyConfigured("You must specify a DB backend to run the app.")

    if not backend in DB_BACKENDS:
        raise ImproperlyConfigured(
            "Unknown DB backend `{backend}`. Must be one out of {keys}".format(
                backend=backend, keys=DB_BACKENDS.keys()
            )
        )

    db_environ_keys = {
        key.replace("SAFEMASKS_DB_", ""): environ.get(key)
        for key in environ
        if key.startswith("SAFEMASKS_DB_")
    }

    missing_keys = DB_BACKENDS[backend]["mandatory_keys"] - db_environ_keys.keys()
    if missing_keys:
        raise ImproperlyConfigured(
            "To use the `{backend}` DB backend, you have to specify {keys}".format(
                backend=backend, keys=["SAFEMASKS_DB_" + key for key in missing_keys]
            )
        )

    if db_environ_keys.pop("SSL", False) and backend != "sqlite":
        db_environ_keys["OPTIONS"] = {"sslmode": "require"}

    return {"ENGINE": DB_BACKENDS[backend]["engine"], **db_environ_keys}


def parse_email_from_environ() -> Dict[str, str]:
    """Parses SAFEMASKS_EMAIL variables from environment to establish connection to the
    mail server
    """
    backend = environ.get("SAFEMASKS_EMAIL_BACKEND", None)

    if not backend:
        raise ImproperlyConfigured("You must specify an email backend to run the app.")

    environ_keys = {
        key.replace("SAFEMASKS_", ""): environ.get(key)
        for key in environ
        if key.startswith("SAFEMASKS_EMAIL_")
    }
    environ_keys["EMAIL_BACKEND"] = EMAIL_BACKENDS[backend]["backend"]

    missing_keys = EMAIL_BACKENDS[backend]["mandatory_keys"] - environ_keys.keys()
    if missing_keys:
        raise ImproperlyConfigured(
            "To use the `{backend}` email backend, you have to specify {keys}".format(
                backend=backend, keys=["SAFEMASKS_DB_" + key for key in missing_keys]
            )
        )

    return environ_keys
