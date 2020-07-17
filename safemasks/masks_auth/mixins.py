from django.contrib.auth.mixins import UserPassesTestMixin

from safemasks.masks_auth.utils import has_verified_email, is_reviewed


class ReviewedRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (
            user
            and user.is_authenticated
            and has_verified_email(user)
            and is_reviewed(user)
        )
