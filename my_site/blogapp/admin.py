from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display: list[str] = [
        "id",
        "title",
        "content_short",
        "pub_date",
        "author",
        "category",
    ]
    ordering: list[str] = ["id", "pub_date"]
    list_display_links: list[str] = ["id", "title"]

    @admin.display(description=_("content"))
    def content_short(self, obj: Article) -> str:
        """The function checks the length of the description within the set length"""
        short_text: str = obj.content if len(obj.content) < 50 else obj.content[:50] + "..."
        return short_text
