"""Automated actions on model modifications
"""
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import User

from safemasks.masks_auth.models import Profile


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):  # pylint: disable=W0613
    """Set user name equal to email since allauth is configured to use mandatory email
    """
    print("pre save")
    if not instance.username:
        instance.username = instance.email


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs):  # pylint: disable=W0613
    """Set user name equal to email since allauth is configured to use mandatory email
    """
    print("post save")
    if not hasattr(instance, "profile"):
        Profile(user=instance, is_reviewed=instance.is_superuser).save()
