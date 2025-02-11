"""
The module comes with a high-level framework for generating XML sitemap files for the model Article.
"""

from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models.query import QuerySet

from .models import Article


class BlogSitemap(Sitemap):
    """
    Class represents a "section" of posts in your sitemap.
    """

    changefreq: str = "never"
    priority: float = 0.5

    def items(self) -> QuerySet[Article]:
        """Method that returns a sequence or QuerySet of objects Article."""
        return (
            Article.objects.filter(pub_date__isnull=False)
            .only("title", "pub_date", "author", "category", "tags")
            .select_related("author", "category")
            .prefetch_related("tags")
            .order_by("-pub_date")
        )

    def lastmod(self, obj: Article) -> datetime:
        """Method that returns the date the object was last modified."""
        return obj.pub_date
