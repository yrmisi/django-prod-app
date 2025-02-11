"""
Models for the shop application.

This module contains the data models for the shop application, including
products and orders. It defines the structure of the database tables and
the relationships between them.
"""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    """
    Generate the file path for product preview images.

    Args:
        instance (Product): The product instance for which the preview is being uploaded.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path for the product preview image.
    """
    return f"products/product_{instance.pk}/preview/{filename}"


class Product(models.Model):
    """
    The product model represents the product sold in the store.

    Orders here: :model:`shop_app.Order`
    """

    name = models.CharField(
        max_length=100, verbose_name=pgettext_lazy("product name", "name"), db_index=True
    )
    description = models.TextField(
        null=False, blank=True, verbose_name=_("description"), db_index=True
    )
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_("price"))
    discount = models.PositiveSmallIntegerField(default=0, verbose_name=_("discount"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    archived = models.BooleanField(default=False, verbose_name=_("archived"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        verbose_name=_("created by"),
    )
    preview = models.ImageField(
        null=True, blank=True, upload_to=product_preview_directory_path, verbose_name=_("preview")
    )

    class Meta:
        """
        Meta options for the Product model.

        Attributes:
            ordering (list): Default ordering for the Product model.
            verbose_name (str): Singular name for the Product model.
            verbose_name_plural (str): Plural name for the Product model.
        """

        ordering = ["name", "price"]
        verbose_name = _("product")  # перевод будет отражен в админ-панели
        verbose_name_plural = _("products")

    def __str__(self) -> str:
        """
        Return a string representation of the product.

        Returns:
            str: A string representation of the product including its name and price.
        """
        # return f"{_('Product')} '{self.name}', {_('price')} {self.price} у.е."
        return _("Product '%(name)s', price %(price)d у.е.") % {
            "name": self.name,
            "price": self.price,
        }

    def get_absolute_url(self) -> str:
        """Returns the absolute URL for the model Product"""
        return reverse("shop_app:product_details", kwargs={"pk": self.pk})


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    """
    Generate the file path for product images.

    Args:
        instance (ProductImage): The product image instance for which the image is being uploaded.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The file path for the product image.
    """
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk, filename=filename
    )


class ProductImage(models.Model):
    """
    The product image model represents images associated with a product.

    Attributes:
        product (Product): The product associated with this image.
        image (ImageField): The image file for the product.
        description (str): A description of the image.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=pgettext_lazy("product id", "product"),
    )
    image = models.ImageField(upload_to=product_images_directory_path, verbose_name=_("image"))
    description = models.CharField(
        max_length=200, null=False, blank=True, verbose_name=_("description")
    )

    class Meta:
        """
        Meta options for the ProductImage model.

        Attributes:
            verbose_name (str): Singular name for the ProductImage model.
            verbose_name_plural (str): Plural name for the ProductImage model.
        """

        verbose_name = _("product image")
        verbose_name_plural = _("product images")

    def __str__(self) -> str:
        """
        Return a string representation of the product image.

        Returns:
            str: A string representation of the product image, indicating
            the associated product's name.
        """
        return _("Product image %s") % (self.product.name,)


class Order(models.Model):
    """
     The order model represents a customer's order containing products and delivery information.

     Products here: :model:`shop_app.Product`

    Attributes:
        user (User ): The user who placed the order.
        products (ManyToManyField): The products included in the order.
        promocode (str): An optional promocode applied to the order.
        delivery_address (str): The address where the order will be delivered.
        created_at (datetime): The timestamp when the order was created.
        receipt (FileField): An optional receipt file associated with the order.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=pgettext_lazy("user id", "user"),
    )
    products = models.ManyToManyField(Product, related_name="orders", verbose_name=_("products"))
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name=_("promocode"))
    delivery_address = models.TextField(verbose_name=_("delivery address"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    receipt = models.FileField(
        verbose_name=_("Receipt"),
        blank=True,
        null=True,
        upload_to="orders/receipts/",
    )

    class Meta:
        """
        Meta options for the Order model.

        Attributes:
            verbose_name (str): Singular name for the Order model.
            verbose_name_plural (str): Plural name for the Order model.
        """

        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self) -> str:
        """
        Return a string representation of the order.

        Returns:
            str: A string representation of the order, including its order number.
        """
        return _("Order № %s") % (self.pk)

    def get_absolute_url(self) -> str:
        """Returns the absolute URL for the model Order"""
        return reverse("shop_app:order_details", kwargs={"pk": self.pk})
