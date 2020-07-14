"""App wide model implementations
"""
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from safemasks.masks_auth.utils import has_verified_email

PHONE_VALIDATOR = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message=_(
        "Phone number must be entered in the format: '+999999999'."
        " Up to 15 digits allowed."
    ),
)


class Profile(models.Model):
    """Extension of the user model
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text=_("User instance."),
        related_name="profile",
        verbose_name=_("User"),
    )
    phone_number = models.CharField(
        validators=[PHONE_VALIDATOR],
        null=True,
        blank=False,
        max_length=17,
        help_text=_("+999999999 Up to 15 digits allowed"),
        verbose_name=_("Phone number"),
    )
    company = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text=_("Name of your company or institution."),
        verbose_name=_("Company"),
    )
    position = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text=_("Position in company or institution."),
        verbose_name=_("Position"),
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=_("Additional information, descriptions and references."),
        verbose_name=_("Description"),
    )
    is_reviewed = models.BooleanField(
        null=False,
        default=False,
        help_text=_("Was the authenticity of the user reviewed by the administration?"),
        verbose_name=_("Is reviewed?"),
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text=_("Ip address associated with user."),
        verbose_name=_("IP address"),
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("Last time the profile was updated."),
        verbose_name=_("Last update"),
    )

    def __str__(self) -> str:
        return f"Profile({self.user})"

    @property
    def has_verified_email(self) -> bool:
        """Checks if at least one email has been verified
        """
        return has_verified_email(self.user)
