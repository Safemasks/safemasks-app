"""Custom implementations of default forms
"""
from django.forms import (
    ModelForm,
    Textarea,
    CharField,
    TextInput,
    ValidationError,
)
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm as AllAuthSignupForm
from ipware import get_client_ip

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from safemasks.masks_auth.models import Profile


class ProfileForm(ModelForm):
    """Form which wraps editable profile attributes
    """

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "company",
            "position",
            "description",
            "accepted_terms",
            "accepted_privacy",
        ]
        widgets = {
            "phone_number": TextInput(attrs={"placeholder": _("+99999 max 15 digits")}),
            "company": TextInput(
                attrs={"placeholder": _("Your company or institution.")}
            ),
            "position": TextInput(
                attrs={"placeholder": _("Your position in this company.")}
            ),
            "description": Textarea(
                attrs={
                    "placeholder": _(
                        "Why are you interested in using safemasks?"
                        " Please add additional descriptions and further links"
                        " to verify your identity."
                    )
                }
            ),
        }
        help_texts = {
            "phone_number": None,
            "company": None,
            "description": None,
            "position": None,
            "accepted_terms": None,
            "accepted_privacy": None,
        }
        labels = {
            "accepted_terms": _(
                """I have read and accept the <a href="#privacy-policy" data-toggle="modal" data-target="#privacy-policy">terms and conditions</a>."""
            ),
            "accepted_privacy": _(
                """I have read and accept the <a href="#privacy-policy" data-toggle="modal" data-target="#privacy-policy">privacy policy</a>."""
            ),
        }


PROFILE_FORM = ProfileForm()


class SignupForm(AllAuthSignupForm):
    """Wraps AllAuth sign up with additional fields for user
    """

    first_name = CharField(
        label=_("First name"),
        max_length=256,
        widget=TextInput(attrs={"placeholder": _("First name")}),
        required=True,
    )
    last_name = CharField(
        label=_("Last name"),
        max_length=256,
        widget=TextInput(attrs={"placeholder": _("Last name")}),
        required=True,
    )

    phone_number = PROFILE_FORM.fields["phone_number"]
    company = PROFILE_FORM.fields["company"]
    position = PROFILE_FORM.fields["position"]
    description = PROFILE_FORM.fields["description"]
    accepted_terms = PROFILE_FORM.fields["accepted_terms"]
    accepted_privacy = PROFILE_FORM.fields["accepted_privacy"]

    def clean_accepted_terms(self):
        data = self.cleaned_data["accepted_terms"]
        if not data:
            raise ValidationError(
                _("You must accept the terms and conditions to register.")
            )
        return data

    def clean_accepted_privacy(self):
        data = self.cleaned_data["accepted_privacy"]
        if not data:
            raise ValidationError(_("You must accept the privacy policy to register."))
        return data

    def save(self, request):
        """Adds additional info to user & user profile
        """
        user = super().save(request)

        if self.cleaned_data["first_name"]:
            user.first_name = self.cleaned_data["first_name"]

        if self.cleaned_data["last_name"]:
            user.last_name = self.cleaned_data["last_name"]

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.ip, _ = get_client_ip(request)
            profile.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("email", css_class="form-group col-md-6 mb-0"),
                Column("phone_number", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("first_name", css_class="form-group col-md-6 mb-0"),
                Column("last_name", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            "company",
            "position",
            "description",
            Row(
                Column("password1", css_class="form-group col-md-6 mb-0"),
                Column("password2", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            "accepted_terms",
            "accepted_privacy",
            Submit("submit", _("Sign Up")),
        )
