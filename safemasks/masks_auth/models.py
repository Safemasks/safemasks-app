"""App wide model implementations
"""
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from safemasks.masks_auth.utils import has_verified_email

PHONE_VALIDATOR = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'."
    " Up to 15 digits allowed.",
)


class Profile(models.Model):
    """Extension of the user model
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="User instance.",
        related_name="profile",
    )
    phone_number = models.CharField(
        validators=[PHONE_VALIDATOR],
        max_length=17,
        null=True,
        blank=True,
        help_text="+999999999 Up to 15 digits allowed",
    )
    company = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="Name of your company or institution.",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Additional information, descriptions and references.",
    )
    is_reviewed = models.BooleanField(
        null=False,
        default=False,
        help_text="Was the authenticity of the user reviewed by the administration?",
    )
    ip = models.GenericIPAddressField(
        null=True, blank=True, help_text="Ip address associated with user."
    )
    last_updated = models.DateTimeField(
        auto_now=True, help_text="Last time the profile was updated."
    )

    def __str__(self) -> str:
        return f"Profile({self.user})"

    @property
    def has_verified_email(self) -> bool:
        """Checks if at least one email has been verified
        """
        return has_verified_email(self.user)
