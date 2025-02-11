"""
This module contains a Django management command for updating orders in the shop application.

The command retrieves the first order from the database and adds all available products to that order.
"""

from typing import Any

from django.core.management import BaseCommand
from shop_app.models import Order, Product


class Command(BaseCommand):
    """Django management command to update an order by adding all products to it."""

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle the command execution.

        This method retrieves the first order from the database and adds all available products
        to that order. If no order is found, an error message is displayed.
        """
        order: Order | None = Order.objects.first()
        if not order:
            self.stdout.write(self.style.ERROR("No order found"))
            return

        products = Product.objects.all()

        for product in products:
            order.products.add(product)

        order.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successful addition products {order.products.all()} to order {order.id}"
            )
        )
