"""
The module comes with a high-level framework for generating XML sitemap files for the model Product.
"""

from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.db.models.query import QuerySet

from .models import Product


class ShopSitemap(Sitemap):
    """
    Class represents a "section" of posts in your sitemap.
    """

    changefreq: str = "daily"
    priority: float = 1.0

    def items(self) -> QuerySet[Product]:
        """Method that returns a sequence or QuerySet of objects Product."""
        return (
            Product.objects.filter(archived=False)
            .only("name", "description", "price", "discount", "preview")
            .order_by("name")
        )

    def lastmod(self, obj: Product) -> datetime:
        """Method that returns the date the object was last modified."""
        return obj.created_at
