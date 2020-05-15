"""Utility functions for auth module
"""
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress


def has_verified_email(user: User) -> bool:
    """Checks if at least one email has been verified for user
    """
    return EmailAddress.objects.filter(user=user, verified=True).exists()


def is_reviwed(user: User) -> bool:
    """Checks if user is reviewed
    """
    return user.profile.is_reviwed
