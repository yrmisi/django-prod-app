"""
This module contains a Django management command for adding a new article
to the database.

The command creates a new article with a specified author, category, and tags.
It ensures that all database operations are atomic by using a transaction.
"""

from datetime import datetime
from typing import Any

from django.core.management import BaseCommand
from django.db import transaction

from ...models import Article, Author, Category, Tag


class Command(BaseCommand):
    """
    Django management command to add a new article to the database.
    """

    help: str = "Adding new article"

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        """Handle the command execution to create a new article."""
        self.stdout.write("Create article")

        author_info: dict[str, str] = {
            "name": "Chuck Arnold",
            "bio": "Senior entertainment writer at the New York Post.",
        }
        author, created = Author.objects.get_or_create(**author_info)

        category_name: str = "Show business"
        category, created = Category.objects.get_or_create(name=category_name)

        tags_info: list[str] = ["Robbie Williams", "films", "musicians"]
        tags: list[Tag] = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_info]

        dt_str: str = "2025-01-10 13:06:00.000000"
        pub_date: datetime = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")

        article_info: dict[str, str | datetime | Author | Category] = {
            "title": "No really, why is Robbie Williams a monkey in the new biopic 'Better Man'?",
            "content": "In 'Better Man' — the new musical biopic of Robbie Williams — the British pop star gets in touch with his inner primate.Indeed, the 50-year-old singer — who rose from the boy band Take That to become one of the biggest UK music icons of the 1990s and early '00s — is transformed into a singing, dancing chimpanzee thanks to the wonders of CGI in the film that opens wide on Friday.",
            "pub_date": pub_date,
            "author": author,
            "category": category,
        }
        article: Article = Article.objects.create(**article_info)
        article.save()

        article.tags.add(*tags)

        self.stdout.write(f"Created new article №{article.pk} ")
