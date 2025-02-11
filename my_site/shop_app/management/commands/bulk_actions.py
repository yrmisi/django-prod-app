"""
This module contains a Django management command for performing bulk actions.

It demonstrates how to efficiently update multiple records in a database with a Product model.
"""

from typing import Any

from django.core.management import BaseCommand

from ...models import Product


class Command(BaseCommand):
    """Django management command to perform bulk actions on products."""

    help: str = "Bulk actions"

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle the command execution.

        This method performs bulk actions on the Product model, such as updating
        the discount for products whose names contain "Smartphone". It also
        demonstrates how to create multiple products in bulk (commented out).
        """
        self.stdout.write("Start demo bulk actions")
        # products_values: list[tuple[str, int]] = [
        #     ("Smartphone 8", 299),
        #     ("Smartphone 9", 399),
        #     ("Smartphone 10", 499),
        # ]
        # products: list[Product] = [
        #     Product(name=name, price=price) for name, price in products_values
        # ]
        # products_created = Product.objects.bulk_create(products)

        # for product in products_created:
        #     print(product)

        count_obj: int = Product.objects.filter(name__contains="Smartphone").update(discount=10)
        print(count_obj)

        self.stdout.write("Done")
