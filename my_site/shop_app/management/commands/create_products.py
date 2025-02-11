"""
This module contains a Django management command for adding products to the Product table in the shop application.

It allows the user to specify the quantity of products to be added, with a limit of 1 to 3 products.
"""

from typing import Any, Mapping

from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from shop_app.models import Product


class Command(BaseCommand):
    """Django management command to add products to the Product table."""

    help = "Adding values to column table Product"

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add command line arguments for the command.

        This method adds an argument to specify the quantity of products to be added to
        the Product table. The quantity must be an integer between 1 and 3.
        """
        parser.add_argument(
            "--quantity", type=int, help="Quantity of goods to fill the table Product"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle the command execution.

        This method retrieves the specified quantity of products and adds them to the Product
        table. If the quantity is not between 1 and 3, an error message is displayed.
        """
        quantity = options.get("quantity")
        if not quantity or quantity > 3:
            self.stdout.write(self.style.ERROR("The quantity of goods must be from 1 to 3"))
            return

        products_names: tuple[Mapping[str, Any], ...] = (
            {
                "name": "Laptop",
                "description": "MacBock Pro 16 Core 10",
                "price": 1999,
                "discount": 5,
            },
            {
                "name": "Desktop",
                "description": "MSI ПК MSI MAG Infinite S3 13TC-853XRU",
                "price": 999,
                "discount": 10,
            },
            {
                "name": "Smartphone",
                "description": "Samsung Exynos 1480, 4x 2.75 GHz ARM Cortex-A78, ARM Cortex-A55",
                "price": 499,
                "discount": 10,
            },
        )
        self.stdout.write("Products:")

        for i in range(quantity):
            product, created = Product.objects.get_or_create(**products_names[i])

            if created:
                action: str = "Created"
            else:
                action = "Extracts"

            self.stdout.write(f"{action} Product: {product.name}")

        self.stdout.write(self.style.SUCCESS(f"Products {action.lower()}"))
