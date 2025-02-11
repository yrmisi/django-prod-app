"""This module contains views for the shop application, including product and order management.

It utilizes Django's class-based views and REST framework viewsets to handle various operations
related to products and orders, including listing, creating, updating, and deleting items.
"""

import logging
from csv import DictWriter
from timeit import default_timer
from typing import Any

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import Group, User
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.forms import Form
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from faker import Faker
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .common import save_csv_file
from .forms import GroupForm, OrderForm, ProductForm
from .models import Order, Product, ProductImage
from .serializers import OrderSerializer, ProductSerializer

logger = logging.getLogger(__name__)
fake: Faker = Faker("ru_RU")


class ShopIndexView(View):
    """
    View to display the main shop index page with available products.

    Methods:
    - get: Handles GET requests to render the shop index template with product data.
    """

    # @method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests for the shop index page.

        This method retrieves a list of products and generates some random text.
        It prepares the context for rendering the shop index template.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered shop index page with the context data.
        """
        products: dict[str, int] = {"smartphone": 3999, "laptop": 4999, "TV": 5999}
        text_rus: list[str] = fake.texts(nb_texts=3)
        context: dict[str, float | int | str | dict[str, int] | list[str]] = {
            "time_running": default_timer(),
            "products": products,
            "items": 1,
            "text_rus": text_rus,
        }
        # print("shop index context:", context)
        logger.debug("Products for shop index: %s", products)
        logger.info("Rendering shop index")
        return render(request, "shop_app/shop-index.html", context=context)


# def index(request: HttpRequest) -> HttpResponse:
#     products: dict[str, int] = {"smartphone": 3999, "laptop": 4999, "TV": 5999}
#     context: dict[str, Any] = {"time_running": default_timer(), "products": products}
#     return render(request, "shop_app/shop-index.html", context=context)


class GroupsListView(View):
    """
    View to manage user groups.

    Methods:
    - get: Renders a list of user groups along with a form for creating new groups.
    - post: Handles form submission to create a new group.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Render the groups list page with a form for creating new groups.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered HTML response containing the groups list and the form.
        """
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related("permissions").all(),
        }
        return render(request, "shop_app/groups-list.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle form submission to create a new user group.

        Args:
            request (HttpRequest): The HTTP request object containing the submitted form data.

        Returns:
            HttpResponse: A redirect to the same page after processing the form.
        """
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        # return self.get(request)
        return redirect(request.path)


# def group_list(request: HttpRequest) -> HttpResponse:
#     context = {"groups": Group.objects.prefetch_related("permissions").all()}
#     return render(request, "shop_app/groups-list.html", context=context)


@extend_schema(description="Product view CRUD")
class ProductViewSet(ModelViewSet):  # type: ignore
    """
    API viewset for managing products.

    Attributes:
    - queryset: The set of products to operate on.
    - serializer_class: The serializer used for product representation.

    Filtering and searching capabilities are enabled through Django filters.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]  # переназначение фильтра в settings.py
    search_fields = ["name", "description"]  # поиск значений входящие в поля
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]  # фильтр по полям
    ordering_fields = ["name", "price", "discount"]  # сортировка по полям

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        """Override parent class ModelViewSet list all products."""
        # print("Hello products list")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get product one by ID",
        description="Retrieves product, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        },
    )
    def retrieve(self, *args: Any, **kwargs: Any):
        """
        Retrieve a product by its ID.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, including the product ID.

        Returns:
            Response: A response containing the product data if found, or a 404 error if not found.
        """
        return super().retrieve(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request) -> HttpResponse:
        """Function download products in .csv file using rest framework django"""
        response: HttpResponse = HttpResponse(content_type="text/csv")
        filename: str = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields: list[str] = ["name", "description", "price", "discount"]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({field: getattr(product, field) for field in fields})

        return response

    @action(methods=["post"], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request) -> Response:
        """
        Function upload products from .csv file using rest framework django, to run,
        you need a command in the terminal
        'curl -X POST -F 'file=@devices.csv' http://127.0.0.1:8000/ru/shop/api/products/upload_csv/'
        """
        products: list[Product] = save_csv_file(
            obj=Product, file=request.FILES["file"].file, encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ProductDetailsView(DetailView):  # type: ignore
    """
    View to display detailed information about a specific product.

    Attributes:
    - template_name: The template used to render product details.
    - queryset: The set of products to retrieve details from.
    """

    template_name = "shop_app/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


# class ProductDetailsView(View):
#     def get(self, request: HttpRequest, pk: int) -> HttpResponse:
#         product = get_object_or_404(Product, pk=pk)
#         context = {"product": product}
#         return render(request, "shop_app/products-details.html", context=context)


class ProductsListView(ListView):  # type: ignore
    """
    View to list all available products.

    Attributes:
    - template_name: The template used to render the list of products.

    Only non-archived products are displayed in this view.
    """

    template_name = "shop_app/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


# class ProductsListView(TemplateView):
#     template_name = "shop_app/products-list.html"

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["products"] = Product.objects.all()
#         return context


# def product_list(request: HttpRequest) -> HttpResponse:
#     context = {"products": Product.objects.all()}
#     return render(request, "shop_app/products-list.html", context=context)


class ProductCreateView(PermissionRequiredMixin, CreateView):  # type: ignore
    """
    View to handle the creation of new products.

    Attributes:
    - permission_required: Permission required to create a product.

    Methods:
    - form_valid: Sets the creator of the product and handles image uploads on successful form submission.
    """

    permission_required = "shop_app.add_product"
    model = Product
    # fields = ["name", "price", "description", "discount", "preview"]
    # либо поля возможно определить с помощью form
    form_class = ProductForm
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("shop_app:product_list")

    def form_valid(self, form: ProductForm) -> HttpResponse:
        """
        Set the creator of the product and handle image uploads on successful form submission.

        Args:
            form (ProductForm): The form that was submitted.

        Returns:
            HttpResponse: A response redirecting to the success URL after the product is created.
        """
        form.instance.created_by = self.request.user
        images = form.cleaned_data["images"]
        for image in images:
            ProductImage.objects.create(product=self.object, image=image)
        return super().form_valid(form)


# def create_product(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form: ProductForm = ProductForm(request.POST)
#         http_status_code: int = 201
#         if form.is_valid():
#             # name = form.cleaned_data("name")
#             # Product.objects.create(**form.cleaned_data)
#             form.save()
#             url = reverse("shop_app:product_list")
#             return redirect(url)
#     else:
#         form = ProductForm()
#         http_status_code = 200

#     context: Dict[str, ProductForm] = {"form": form}
#     return render(
#         request=request,
#         template_name="shop_app/create-product.html",
#         context=context,
#         status=http_status_code,
#     )


class ProductUpdateView(UserPassesTestMixin, UpdateView):  # type: ignore
    """
    View to manage updates to existing products.

    Methods:
    - test_func: Checks if the user has permission to update the product based on ownership or admin status.
    - get_success_url: Returns the URL to redirect after successful update.
    - form_valid: Handles image uploads on successful form submission.
    """

    model = Product
    # fields = ["name", "price", "description", "discount", "preview"]
    form_class = ProductForm
    template_name_suffix = "_update_form"
    # success_url = reverse_lazy("shop_app:product_list")

    def test_func(self) -> bool:
        """
        Check if the user has permission to update the product.

        Returns:
            bool: True if the user is a superuser or has edit permission and is the creator
            of the product, False otherwise.
        """
        if self.request.user.is_superuser:
            return True

        self.object = self.get_object()

        has_edit_perm = self.request.user.has_perm("shop_app.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

    # метод get_success_url не нужен при написании в модели Product метода get_absolute_url
    # def get_success_url(self) -> str:
    #     """
    #     Return the URL to redirect to after a successful product update.

    #     Returns:
    #         str: The URL to the product details page for the updated product.
    #     """
    #     return reverse("shop_app:product_details", kwargs={"pk": self.object.pk})

    def form_valid(self, form: ProductForm) -> HttpResponse:
        """
        Handle the form submission and process image uploads.

        Args:
            form (ProductForm): The form that was submitted.

        Returns:
            HttpResponse: A response redirecting to the success URL after processing the form.
        """
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(product=self.object, image=image)
        return response


class ProductDeleteView(UserPassesTestMixin, DeleteView):  # type: ignore
    """
    View to handle archiving (deletion) of products.

    Methods:
    - test_func: Checks if the user has permission to delete this product based on ownership or admin status.
    - form_valid: Archives the product instead of deleting it from the database.
    """

    model = Product
    template_name_suffix = "_archived"
    success_url = reverse_lazy("shop_app:product_list")

    def test_func(self) -> bool:
        """
        Check if the user has permission to delete (archive) the product.

        Returns:
            bool: True if the user is a superuser or has edit permission and is the creator
            of the product, False otherwise.
        """
        if self.request.user.is_superuser:
            return True

        self.object = self.get_object()

        has_edit_perm = self.request.user.has_perm("shop_app.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        """
        Archive the product instead of deleting it from the database.

        Args:
            form (Form): The form that was submitted.

        Returns:
            HttpResponseRedirect: A redirect to the success URL after archiving the product.
        """
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    """
    View to export product data in JSON format.

    Methods:
    - get: Handles GET requests and returns a JSON response containing all product data.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Handle GET requests to export product data in JSON format.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing all product data, including
            product primary key, name, price, and archived status.
        """
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)

        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = {
                "products": [
                    {
                        "pk": product.pk,
                        "name": product.name,
                        "price": product.price,
                        "archived": product.archived,
                    }
                    for product in products
                ]
            }
            elem = products_data["products"][0]
            product_name = elem["name"]
            print(product_name)
            cache.set(cache_key, products_data, 300)

        return JsonResponse(products_data, safe=False)


class LatestProductsFeed(Feed):
    """
    Class for displaying the RSS feed of products in the store.
    """

    title: str = _("Products in the store")
    link: str = reverse_lazy("shop_app:product_list")
    description: str = _("Current products sold in the store.")

    def items(self) -> QuerySet[Product]:
        """Returns a QuerySet of objects Product."""
        return (
            Product.objects.filter(archived=False)
            .only("name", "description", "price", "discount")
            .order_by("-created_at")[:30]
        )

    def item_title(self, item: Product) -> str:
        """Returns the product name to the feed."""
        return item.name

    def item_description(self, item: Product) -> str:
        """Returns a shortened description of the product to the feed."""
        short_description = (
            item.description if len(item.description) < 30 else item.description[:30] + "..."
        )
        return short_description


class OrderViewSet(ModelViewSet):  # type: ignore
    """
    API viewset for managing orders.

    Attributes:
    - queryset: The set of orders to operate on.
    - serializer_class: The serializer used for order representation.

    Filtering and searching capabilities are enabled through Django filters.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]  # переназначение фильтра в settings.py
    search_fields = [
        "user",
        "products",
        "delivery_address",
    ]  # поиск значений входящие в поля
    filterset_fields = [
        "user",
        "products",
        "promocode",
        "delivery_address",
    ]  # фильтр по полям
    ordering_fields = ["user", "delivery_address"]  # сортировка по полям


class OrdersListView(LoginRequiredMixin, ListView):  # type: ignore
    """
    View to list all orders for logged-in users.

    Attributes:
    - queryset: The set of orders associated with users that are logged in.

    This view ensures that only authenticated users can access their order history.
    """

    queryset = Order.objects.select_related("user").prefetch_related("products")
    # context_object_name = "orders"


# def order_list(request: HttpRequest) -> HttpResponse:
#     context = {"orders": Order.objects.select_related("user").prefetch_related("products").all()}
#     return render(request, "shop_app/orders-list.html", context=context)


class OrdersDetailView(PermissionRequiredMixin, DetailView):  # type: ignore
    """
    View to display detailed information about a specific order.

    Attributes:
    - permission_required: Permission required to view an order detail.

    This view ensures that only authorized users can access order details.
    """

    permission_required = "shop_app.view_order"
    queryset = Order.objects.select_related("user").prefetch_related("products")


class OrderCreateView(CreateView):  # type: ignore
    """
    View to handle the creation of new orders.

    Attributes:
    - form_class: The form used for creating an order.
    - template_name: The template used for rendering order creation page.
    """

    # model = Order
    form_class = OrderForm
    template_name = "shop_app/order_create.html"
    success_url = reverse_lazy("shop_app:order_list")


# def create_order(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form: OrderForm = OrderForm(request.POST)
#         http_status_code: int = 201
#         if form.is_valid():
#             form.save()
#             url = reverse("shop_app:order_list")
#             return redirect(url)

#     else:
#         form = OrderForm()
#         http_status_code = 200

#     context: Dict[str, OrderForm] = {"form": form}
#     return render(
#         request=request,
#         template_name="shop_app/create-order.html",
#         context=context,
#         status=http_status_code,
#     )


class OrderUpdateView(UpdateView):  # type: ignore
    """
    View to manage updates to existing orders.

    Attributes:
    - model: The order model being updated.
    - form_class: The form used for updating an order.

    Methods:
    - get_success_url(): Returns URL to redirect after successful update.
    """

    model = Order
    form_class = OrderForm
    template_name_suffix = "_update"

    # комитем метод, т.к. прописан метод get_absolute_url в модели Order
    # def get_success_url(self) -> str:
    #     """
    #     Return the URL to redirect to after a successful order update.

    #     Returns:
    #         str: The URL to the order details page for the updated order.
    #     """
    #     return reverse("shop_app:order_details", kwargs={"pk": self.object.pk})


class OrderDeleteView(DeleteView):  # type: ignore
    """
    View to handle deletion of orders.

    Attributes:
    - model: The order model being deleted.

    This view allows users with appropriate permissions to delete their orders.
    """

    model = Order
    template_name_suffix = "_delete"
    success_url = reverse_lazy("shop_app:order_list")


# TDD
class OrdersDataExportView(UserPassesTestMixin, View):
    """
    Export order data in JSON format with permission checks.

    Methods:
    - test_func(): Checks if the user is staff before allowing access.
    - get(): Handles GET requests and returns a JSON response containing all order data.
    """

    def test_func(self) -> bool:
        """
        Checks if the user is staff.

        Returns:
            bool: True if the user is a staff member, False otherwise.
        """
        return True if self.request.user.is_staff else False

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Export order data in JSON format for GET requests.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing all order data, including
            order primary key, user primary key, product primary keys,
            promocode, and delivery address.
        """
        orders = Order.objects.order_by("pk").all()
        orders_data = {
            "orders": [
                {
                    "pk": order.pk,
                    "user": order.user.pk,
                    "products": [product.pk for product in order.products.all()],
                    "promocode": order.promocode,
                    "delivery_address": order.delivery_address,
                }
                for order in orders
            ]
        }
        return JsonResponse(orders_data, safe=False)


class UserOrdersListView(LoginRequiredMixin, ListView):
    """
    Page with the list of orders of the current user.
    """

    model: Order = Order
    context_object_name: str = "user_order_list"
    template_name: str = "shop_app/user_orders_list.html"

    @property
    def owner(self):
        """Returns the specified user with caching."""
        if not hasattr(self, "_owner"):
            user_id: int | None = self.kwargs.get("user_id")

            if not user_id:
                raise Http404(_("User ID is missing."))

            try:
                self._owner: User = get_object_or_404(User, pk=user_id)
            except Http404:
                raise Http404(_("User with the specified ID not found."))

        return self._owner

    def get_queryset(self):
        """Returns a list of orders for the specified user."""
        return (
            Order.objects.filter(user=self.owner)
            .select_related("user")
            .prefetch_related("products")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Adding user information to the context."""
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class UserOrdersExportView(View):
    """
    Page with a list of orders of the installed user in JSON format.
    """

    def _get_user(self, user_id: int) -> User:
        """Returns the user by ID or throws a 404 error."""
        if not user_id:
            raise Http404(_("User ID is missing."))
        return get_object_or_404(User, pk=user_id)

    def get(self, request: HttpRequest, user_id: int) -> JsonResponse:
        """Returns a JSON response with the list of orders for the specified user by ID."""
        cache_key: str = "user_orders_data_export" + str(user_id)
        user_orders_data: dict[str, dict[str, int | str | list[int]]] | None = cache.get(cache_key)

        if user_orders_data is None:
            user: User = self._get_user(user_id)
            user_orders: Order = (
                Order.objects.filter(user=user)
                .select_related("user")
                .prefetch_related(
                    Prefetch("products", queryset=Product.objects.only("pk").order_by("pk"))
                )
                .order_by("pk")
            )
            key_user_orders: str = user.username + "_orders"
            user_orders_data: dict[str, dict[str, int | str | list[int]]] = {
                key_user_orders: [
                    {
                        "pk": order.pk,
                        "created_at": order.created_at,
                        "promocode": order.promocode,
                        "delivery_address": order.delivery_address,
                        "products": ([product.pk for product in order.products.all()]),
                        "receipt": order.receipt.path if order.receipt else None,
                    }
                    for order in user_orders
                ]
            }
            cache.set(cache_key, user_orders_data, 300)
        return JsonResponse(data=user_orders_data, safe=False)
