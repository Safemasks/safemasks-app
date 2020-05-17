"""Automated actions on model modifications
"""
from django.dispatch import receiver
from django.db.models.signals import pre_save

from django.contrib.auth.models import User


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):  # pylint: disable=W0613
    """Set user name equal to email since allauth is configured to use mandatory email
    """
    instance.username = instance.email
