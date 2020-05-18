"""Custom implementations of default forms
"""
from django.forms import ModelForm, Textarea, CharField, TextInput

from allauth.account.forms import SignupForm as AllAuthSignupForm
from ipware import get_client_ip

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from masks_auth.models import Profile


class ProfileForm(ModelForm):
    """Form which wraps editable profile attributes
    """

    class Meta:
        model = Profile
        fields = ["phone_number", "company", "description"]
        widgets = {
            "phone_number": TextInput(attrs={"placeholder": "+99999 max 15 digits"}),
            "company": TextInput(attrs={"placeholder": "Your company or institution."}),
            "description": Textarea(
                attrs={
                    "placeholder": "Why are you interested in using Safe Masks?"
                    " Please add additional descriptions and further links"
                    " to verify your identity."
                }
            ),
        }
        help_texts = {
            "phone_number": None,
            "company": None,
            "description": None,
        }


PROFILE_FORM = ProfileForm()


class SignupForm(AllAuthSignupForm):
    """Wraps AllAuth sign up with additional fields for user
    """

    first_name = CharField(
        max_length=256,
        widget=TextInput(attrs={"placeholder": "First name"}),
        required=True,
    )
    last_name = CharField(
        max_length=256,
        widget=TextInput(attrs={"placeholder": "Last name"}),
        required=True,
    )

    phone_number = PROFILE_FORM.fields["phone_number"]
    company = PROFILE_FORM.fields["company"]
    description = PROFILE_FORM.fields["description"]

    def save(self, request):
        """Adds additional info to user & user profile
        """
        user = super().save(request)

        if self.cleaned_data["first_name"]:
            user.first_name = self.cleaned_data["first_name"]

        if self.cleaned_data["last_name"]:
            user.last_name = self.cleaned_data["last_name"]

        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)

            profile.user = user
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
            "description",
            Row(
                Column("password1", css_class="form-group col-md-6 mb-0"),
                Column("password2", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Sign Up"),
        )
