"""
This module contains a Django management command for creating a single order.

The order is created with randomly selected products for a randomly selected user.
"""

from random import choice, choices
from typing import Any, Sequence

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from shop_app.models import Order, Product


class Command(BaseCommand):
    """Django management command to create one order with random products."""

    help: str = "Create one order"

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle the command execution.

        This method creates a single order for a randomly selected user with
        three randomly selected products. The order is saved to the database.
        """
        self.stdout.write("Create one order with products")

        username_all: list[str] = list(User.objects.values_list("username", flat=True))
        username_random: str = choice(username_all)
        user: User = User.objects.get(username=username_random)
        # products: Sequence[Product] = Product.objects.all()
        # products: Sequence[Product] = Product.objects.defer(
        #     "description", "price", "created_at"
        # ).all()
        # products: Sequence[Product] = Product.objects.only("id").all()
        ids_all: list[int] = list(Product.objects.values_list("pk", flat=True))
        ids_random: list[int] = choices(ids_all, k=3)
        products_random: Sequence[Product] = Product.objects.filter(pk__in=ids_random)
        order, created = Order.objects.get_or_create(
            delivery_address="Penza, st.M.Lomonosova, h.15", promocode="Sale10", user=user
        )

        for product in products_random:
            order.products.add(product)
        order.save()

        self.stdout.write(f"Created new order {order}")
