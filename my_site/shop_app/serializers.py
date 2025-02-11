"""
Serializers for the shop application.

This module contains serializers for the Product and Order models.
Serializers are used to convert complex data types, such as querysets
and model instances, into native Python data types that can then be
rendered into JSON or other content types. They also handle validation
of incoming data.
"""

from rest_framework import serializers

from .models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer converts Product model instances into JSON format
    and validates incoming data for creating or updating products.

    Meta:
        model: The Product model to serialize.
        exclude: Fields to exclude from serialization (e.g., created_by).
    """

    class Meta:
        """
        Meta class for ProductSerializer.

        This class contains configuration options for the serializer.

        Attributes:
            model (Product): The Product model to serialize.
            exclude (list): Fields to exclude from serialization (e.g., created_by).
        """

        model = Product
        exclude = ["created_by"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    This serializer converts Order model instances into JSON format
    and validates incoming data for creating or updating orders.

    Meta:
        model: The Order model to serialize.
        fields: All fields of the Order model will be included in the serialization.
    """

    class Meta:
        """
        Meta class for OrderSerializer.

        This class contains configuration options for the serializer.

        Attributes:
            model (Order): The Order model to serialize.
            fields (str): All fields of the Order model will be included in the serialization.
        """

        model = Order
        fields = "__all__"
