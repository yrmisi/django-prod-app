"""
This module contains views for displaying articles in a Django application.
It includes a list view for multiple articles and a detail view for a single article.
"""

from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from .models import Article


class ArticleListView(ListView):
    """
    View to display a list of articles.
    This view retrieves a queryset of articles, including their titles, publication dates,
    authors, categories, and tags. The articles are ordered by publication date.
    """

    context_object_name = "articles"
    queryset = (
        Article.objects.filter(pub_date__isnull=False)
        .only("title", "pub_date", "author", "category", "tags")
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-pub_date")
    )


class ArticleDetailView(DetailView):
    """
    View to display the details of a single article.
    This view retrieves an article's title, publication date, author, and content,
    along with any associated tags.
    """

    context_object_name = "article"
    queryset = (
        Article.objects.only("title", "pub_date", "author", "content")
        .select_related("author")
        .prefetch_related("tags")
    )


class LatestArticlesFeed(Feed):
    """
    Class for displaying news feed RSS.
    """

    title: str = _("Blog articles (latest)")
    description: str = _("Updates on changes and addition blog articles")
    link: str = reverse_lazy("blogapp:article_list")

    def items(self):
        return (
            Article.objects.filter(pub_date__isnull=False)
            .only("title", "pub_date", "author", "category", "tags")
            .select_related("author", "category")
            .prefetch_related("tags")
            .order_by("-pub_date")[:5]
        )

    def item_title(self, item: Article) -> str:
        return item.title

    def item_description(self, item: Article) -> str:
        short_content = item.content[:100] + ("" if len(item.content) < 100 else "...")
        return short_content

    # при прокисании метода get_absolute_url в модели Article данный метод можно не использовать
    # def item_link(self, item: Article):
    #     return reverse("blogapp:article_details", kwargs={"pk": item.pk})
