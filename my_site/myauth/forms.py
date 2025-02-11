from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": _("First name"), "last_name": _("Last name"), "email": _("E-mail")}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "agreement_accepted", "avatar"]
        labels = {
            "bio": _("Biography"),
            "agreement_accepted": _("Agreement"),
            "avatar": _("Add avatar"),
        }


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        labels = {"avatar": _("Change avatar")}
