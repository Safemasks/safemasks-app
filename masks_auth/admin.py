"""Extensions of the admin page
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from masks_auth.models import Profile


class ProfileInline(admin.StackedInline):
    """Profile addition to user
    """

    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    """Extends user admin with profile
    """

    inlines = (ProfileInline,)
    list_display = (*BaseUserAdmin.list_display, "is_reviewed")
    list_filter = (*BaseUserAdmin.list_filter, "profile__is_reviewed")

    def is_reviewed(self, obj) -> bool:  # pylint:disable=R0201
        """Returns if profile is reviewed
        """
        return obj.profile.is_reviewed

    is_reviewed.boolean = True
    is_reviewed.short_description = "Is reviewed"
    is_reviewed.admin_order_field = "profile__is_reviewed"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
