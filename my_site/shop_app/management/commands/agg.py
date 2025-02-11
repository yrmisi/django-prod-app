"""
This module contains management command for demonstrating aggregate functions on the Order and Product models.

It showcases how to calculate various statistics such as total price and product count for orders.
"""

from typing import Any

from django.core.management import BaseCommand
from django.db.models import Count, Sum

from ...models import Order


class Command(BaseCommand):
    """Django management command to demonstrate aggregate functions on orders."""

    help: str = "Aggregate functions"

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle the command execution.

        This method retrieves orders and annotates them with the total price of products
        and the count of products in each order. It then prints the details of each order
        to the console.
        """
        self.stdout.write("Start demo aggregate")
        # result = Product.objects.filter(name__contains="Smartphone").aggregate(
        #     Avg("price"), Max("price"), price_min=Min("price"), count=Count("id")
        # )
        # print(result)

        orders = Order.objects.annotate(
            total=Sum("products__price", default=0), products_count=Count("products")
        )

        for order in orders:
            print(f"Order № {order.pk} with {order.products_count} products worth {order.total}")

        self.stdout.write("Done")
