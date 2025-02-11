"""
This module contains a Django command to manage a field from the User model in Django authentication system.

It demonstrates the use of `values_list` to retrieve usernames and user primary keys.
"""

from typing import Any

from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Django management command to demonstrate field selection from the User model."""

    help: str = "Selecting fields"

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Execute the command to select and display user fields.

        This method retrieves usernames and primary keys from the User model and prints them
        to the console. It demonstrates the use of `values_list` for efficient data retrieval.
        """
        self.stdout.write("Start demo select fields")
        users_one_field = User.objects.values_list("username", flat=True).order_by("pk")
        print(list(users_one_field))

        users_info = User.objects.values_list("pk", "username").order_by("pk")
        for user_info in users_info:
            print(*user_info, sep=". ")

        # product_values = Product.objects.values("pk", "name")

        # for p_val in product_values:
        #     print(p_val)

        self.stdout.write("Done")
