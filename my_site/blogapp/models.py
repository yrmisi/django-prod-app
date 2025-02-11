"""
This module defines the data models for a blogging application using Django's ORM.
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, pgettext_lazy


class Author(models.Model):
    """
    Represents an author of articles.
    """

    name = models.CharField(
        max_length=100, verbose_name=pgettext_lazy("author name", "name"), db_index=True
    )
    bio = models.TextField(blank=True, verbose_name=_("biography"))

    class Meta:
        """
        Meta options for the Author model.
        """

        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self):
        """Returns a string representation of the Author instance."""
        return _("Author %(name)s by id %(pk)d") % {"name": self.name, "pk": self.pk}


class Category(models.Model):
    """
    Represents a category for articles.
    """

    name = models.CharField(
        max_length=40, verbose_name=pgettext_lazy("category name", "name"), db_index=True
    )

    class Meta:
        """
        Meta options for the Category model.
        """

        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        """Returns a string representation of the Category instance."""
        return _("Category %(name)s by id %(pk)d") % {"name": self.name, "pk": self.pk}


class Tag(models.Model):
    """
    Represents a tag that can be associated with articles.
    """

    name = models.CharField(
        max_length=20, verbose_name=pgettext_lazy("tag name", "name"), db_index=True
    )

    class Meta:
        """
        Meta options for the Tag model.
        """

        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        """Returns a string representation of the Tag instance."""
        return _("Tag with id-%(pk)d by %(name)s") % {"pk": self.pk, "name": self.name}


class Article(models.Model):
    """
    Represents an article written by an author.
    """

    title = models.CharField(max_length=200, verbose_name=_("title"), db_index=True)
    content = models.TextField(verbose_name=_("content"))
    pub_date = models.DateTimeField(null=True, blank=True, verbose_name=_("date of publication"))
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="article_authors",
        verbose_name=_("authors id"),
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="article_categories",
        verbose_name=_("category id"),
        db_index=True,
    )
    tags = models.ManyToManyField(Tag, related_name="article_tags", verbose_name=_("tags"))

    class Meta:
        """
        Meta options for the Article model.
        """

        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self):
        """
        Returns a string representation of the Article instance.
        """
        return _("Article with id-%(pk)d title %(title)s from the author by id %(author_id)s") % {
            "pk": self.pk,
            "title": self.title,
            "author_id": self.author,
        }

    def get_absolute_url(self) -> str:
        return reverse("blogapp:article_details", kwargs={"pk": self.pk})
