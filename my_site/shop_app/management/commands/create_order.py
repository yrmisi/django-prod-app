"""
This module contains a Django management command for creating orders in the shop application.

It allows the user to specify a username, delivery address, and promocode for the order.
"""

from typing import Any

from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError
from django.core.management.base import CommandParser
from shop_app.models import Order


class Command(BaseCommand):
    """Django management command to create an order for a user."""

    help: str = "Create order"

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add command line arguments for the command.

        This method adds arguments to specify the username, delivery address, and promocode
        for the order being created.
        """
        parser.add_argument("--username", type=str, help="Create user name")
        parser.add_argument("--delivery_address", type=str, help="Delivery address")
        parser.add_argument("--promocode", type=str, help="Promocode")

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Handle the command execution.

        This method retrieves the user by username, creates an order with the specified
        delivery address and promocode, and outputs the result to the console. If the user
        does not exist, an error is raised.
        """
        username: str = options["username"]
        delivery_address: str = options["delivery_address"]
        promocode: str = options["promocode"]

        if not username:
            self.stdout.write(self.style.ERROR("User name missing"))
            return

        self.stdout.write("Create order")
        try:
            user: User = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError('User "%s" does not exist' % username)

        order, created = Order.objects.get_or_create(
            delivery_address=delivery_address, promocode=promocode, user=user
        )

        if created:
            action: str = "created"
        else:
            action = "extracts"

        self.stdout.write(f"Order {action} {order.id}")
