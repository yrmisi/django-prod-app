"""
The module comes with a high-level framework for generating XML sitemap files for the model Profile.
"""

from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models.functions import Lower
from django.db.models.query import QuerySet

from .models import Profile


class ProfileSitemap(Sitemap):
    """
    Class represents a "section" of posts in your sitemap.
    """

    changefreq: str = "hourly"
    priority: float = 0.8

    def items(self) -> QuerySet[Profile]:
        """Method that returns a sequence or QuerySet of objects Profile."""
        return (
            Profile.objects.only("user", "bio", "avatar")
            .select_related("user")
            .order_by(Lower("user__username"))
        )

    def lastmod(self, obj: Profile) -> datetime:
        """Method that returns the date the object was last modified."""
        return obj.user.date_joined
