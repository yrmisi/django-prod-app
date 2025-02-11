from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return f"profiles/user_{instance.user.pk}/avatar/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    bio = models.TextField(max_length=500, blank=True, verbose_name=_("biography"))
    agreement_accepted = models.BooleanField(default=False, verbose_name=_("agreement accepted"))
    avatar = models.ImageField(
        verbose_name=_("avatar"), null=True, blank=True, upload_to=profile_avatar_directory_path
    )

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self) -> str:
        return _("User profile id %d") % (self.pk,)

    def get_absolute_url(self) -> str:
        return reverse("myauth:profiles_detail", kwargs={"pk": self.pk})
