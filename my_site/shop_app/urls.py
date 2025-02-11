"""
URL configuration for the shop application.

This module defines the URL patterns for the shop application, including
views for managing products, orders, and user groups. It uses Django's
path and include functions to route requests to the appropriate views.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    GroupsListView,
    LatestProductsFeed,
    OrderCreateView,
    OrderDeleteView,
    OrdersDataExportView,
    OrdersDetailView,
    OrdersListView,
    OrderUpdateView,
    OrderViewSet,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailsView,
    ProductsDataExportView,
    ProductsListView,
    ProductUpdateView,
    ProductViewSet,
    ShopIndexView,
    UserOrdersExportView,
    UserOrdersListView,
)

app_name: str = "shop_app"

routers = DefaultRouter()
routers.register(r"products", ProductViewSet, basename="product_set")
routers.register(r"orders", OrderViewSet, basename="order_set")

urlpatterns = [
    # path("", cache_page(60 * 3)(ShopIndexView.as_view()), name="index"),
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="group_list"),
    path("api/", include(routers.urls)),
    path("products/", ProductsListView.as_view(), name="product_list"),
    path("products/export/", ProductsDataExportView.as_view(), name="product_export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archived/", ProductDeleteView.as_view(), name="product_archived"),
    path("products/latest/feed/", LatestProductsFeed(), name="product_feed"),
    path("orders/", OrdersListView.as_view(), name="order_list"),
    path("orders/export/", OrdersDataExportView.as_view(), name="order_export"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="user_orders_list"),
    path(
        "users/<int:user_id>/orders/export/",
        UserOrdersExportView.as_view(),
        name="user_orders_export",
    ),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
