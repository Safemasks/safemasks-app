"""Additional permissions for access levels
"""

from rest_framework.permissions import IsAuthenticated


class IsReviewed(IsAuthenticated):
    """Extend regulare IsAuthenticated permission with selected access rights
    """

    def has_permission(self, request, view):
        """Checks if the user was reviewed in top of authenticated
        """
        return (
            super().has_permission(request, view) and request.user.profile.is_reviewed
        )
