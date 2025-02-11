from typing import Dict, List, Tuple

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import URLPattern, path
from django.utils.translation import gettext_lazy as _

from .admin_mixins import ExportAsCSVMixin
from .common import save_csv_file, save_json_file
from .forms import FileImportForm
from .models import Order, Product, ProductImage


class OrderInline(admin.TabularInline):
    model = Product.orders.through
    extra = 0  # удаляет три пустых строки в Order-product relationships
    verbose_name = _("order")
    verbose_name_plural = _("orders")


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.action(description="Archive product")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """Function for group action archiving"""
    queryset.update(archived=True)


@admin.action(description="Unarchive product")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """Function for group action unzip"""
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    list_display: list[str] = [
        "id",
        "name",
        "description_short",
        "price",
        "discount",
        "archived",
    ]  # поля для отоброжения в админке
    list_display_links: list[str] = ["id", "name"]  # определяет поля для перехода кликом
    ordering: list[str] = ["id"]  # сортировка по
    search_fields: List[str] = [
        "id",
        "name",
        "description",
    ]  # устанавливаем поля, по которым идет поиск
    inlines: list[OrderInline] = [OrderInline, ProductImageInline]  # связь Many to Many
    fieldsets: list[Tuple[None | str | Dict]] = [
        (None, {"fields": ("name", "description")}),
        (_("Price options"), {"fields": ("price", "discount"), "classes": ("collapse", "wide")}),
        (_("Images"), {"fields": ("preview",)}),
        (
            _("Extra options"),
            {
                "fields": ("archived",),
                "classes": ("collapse",),
                "description": _("Extra options. Field 'archived' is for soft delete"),
            },
        ),
    ]  # группировка и скрытие полей
    actions: list[str] = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]  # групповое действие для записей
    change_list_template: str = "shop_app/shop_changelist.html"

    def description_short(self, obj: Product) -> str:
        """The function checks the length of the description within the set length"""
        if len(obj.description) < 30:
            return obj.description
        return obj.description[:30] + "..."

    description_short.short_description = _(
        "Product characteristics"
    )  # изменение названия колонки с 'Description short' на 'Product characteristics'"

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form: FileImportForm = FileImportForm()
            context: dict[str, FileImportForm | bool] = {"form": form, "file_csv": True}
            return render(
                request=request, template_name="admin/csv_or_json_form.html", context=context
            )

        form: FileImportForm = FileImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context: dict[str, FileImportForm] = {"form": form}
            return render(
                request=request,
                template_name="admin/csv_or_json_form.html",
                context=context,
                status=400,
            )
        uploaded_file = form.files["uploaded_file"]
        base_message: str = _("Data from %s was imported")
        level_message: int = messages.SUCCESS
        redirect_url: str = ".."

        if uploaded_file.name.endswith(".csv"):
            save_csv_file(obj=Product, file=uploaded_file.file, encoding=request.encoding)
            loading_message = base_message % "CSV"
        else:
            file_extension: str = request.path[request.path.rfind("-") + 1 : -1]
            loading_message = _("The file must have the %s extension") % file_extension
            level_message = messages.ERROR
            redirect_url = "."

        self.message_user(request, loading_message, level=level_message)
        return redirect(redirect_url)

    def get_urls(self):
        urls = super().get_urls()
        new_urls: list[URLPattern] = [
            path("import-products-csv/", self.import_csv, name="import_products_csv")
        ]
        return new_urls + urls

    def changelist_view(self, request: HttpRequest, extra_context=None):
        """Create an additional context and call the parent method with the additional context."""
        extra_context = extra_context or {}
        extra_context["url_import_csv"] = "admin:import_products_csv"
        return super().changelist_view(request, extra_context=extra_context)


# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through
    extra = 0
    verbose_name = _("product")
    verbose_name_plural = _("products")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: list[str] = ["id", "delivery_address", "promocode", "created_at", "user_verbose"]
    list_display_links: list[str] = ["id", "delivery_address"]
    ordering: list[str] = ["id"]
    search_fields: list[str] = ["id", "delivery_address", "promocode"]
    inlines: list[ProductInline] = [ProductInline]  # связь Many to Many
    fieldsets: list[tuple[str, dict[str, list[str]]]] = [
        (
            _("Shipping information"),
            {"fields": ["delivery_address", "user", "receipt"], "classes": ["wide"]},
        ),
    ]
    change_list_template: str = "shop_app/shop_changelist.html"

    def get_queryset(self, request: HttpRequest) -> QuerySet[Order]:
        """The function loading in one request 'user'"""
        return Order.objects.select_related("user").prefetch_related("products")

    @admin.display(description=_("User"))
    def user_verbose(self, obj: Order) -> str:
        """The function returns the user name or username"""
        return obj.user.first_name or obj.user.username

    # user_verbose.short_description = _("User")

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form: FileImportForm = FileImportForm()
            context: dict[str, FileImportForm | bool] = {"form": form}

            if request.path.endswith("-csv/"):
                context["file_csv"] = True
            elif request.path.endswith("-json/"):
                context["file_json"] = True
            return render(
                request=request, template_name="admin/csv_or_json_form.html", context=context
            )

        form = FileImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context: dict[str, FileImportForm] = {"form": form}
            return render(
                request=request,
                template_name="admin/csv_or_json_form.html",
                context=context,
                status=400,
            )
        uploaded_file = form.files["uploaded_file"]
        redirect_url: str = ".."
        base_message: str = _("Data from %s was imported")
        level_message: int = messages.SUCCESS

        if uploaded_file.name.endswith(".csv"):
            save_csv_file(
                obj=Order,
                file=uploaded_file.file,
                encoding=request.encoding,
                exclude_key="products",
            )
            loading_message: str = base_message % "CSV"
        elif uploaded_file.name.endswith(".json"):
            save_json_file(
                obj=Order,
                file=uploaded_file.file,
                encoding=request.encoding,
                exclude_key="products",
            )
            loading_message = base_message % "JSON"
        else:
            file_extension: str = request.path[request.path.rfind("-") + 1 : -1]
            loading_message = _("The file must have the %s extension") % file_extension
            level_message = messages.ERROR
            redirect_url = "."

        self.message_user(request, loading_message, level=level_message)
        return redirect(redirect_url)

    def get_urls(self):
        urls = super().get_urls()
        new_urls: list[URLPattern] = [
            path("import-orders-json/", self.import_csv, name="import_orders_json"),
            path("import-orders-csv/", self.import_csv, name="import_orders_csv"),
        ]
        return new_urls + urls

    def changelist_view(self, request: HttpRequest, extra_context=None):
        """Create an additional context and call the parent method with the additional context."""
        extra_context = extra_context or {}
        extra_context["url_import_csv"] = "admin:import_orders_csv"
        extra_context["url_import_json"] = "admin:import_orders_json"
        return super().changelist_view(request, extra_context=extra_context)


# admin.site.register(Product, ProductAdmin, Order, OrderAdmin)
