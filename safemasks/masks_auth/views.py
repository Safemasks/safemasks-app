from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from safemasks.masks_auth.models import Profile
from safemasks.masks_auth.forms import PROFILE_FORM


class ProfileView(UpdateView, LoginRequiredMixin):
    """View of profile for logged in users
    """

    model = Profile
    template_name = "account/profile.html"
    fields = [
        "phone_number",
        "company",
        "position",
        "description",
    ]
    success_url = reverse_lazy("masks_auth:profile")

    def get_object(self, queryset=None):
        """Returns the profile of currently logged in user
        """
        return self.request.user.profile
