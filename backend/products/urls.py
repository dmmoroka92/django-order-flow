from django.urls import path

from products.views import (
    InventoryDetailView,
    InventoryListCreateView,
    ProductDetailView,
    ProductListCreateView,
    RemoveStockView,
    RestockInventoryView,
)

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("inventories/", InventoryListCreateView.as_view(), name="inventory-list"),
    path("inventories/<int:pk>/", InventoryDetailView.as_view(), name="inventory-detail"),
    path("inventories/<int:pk>/restock/", RestockInventoryView.as_view(), name="inventory-restock"),
    path(
        "inventories/<int:pk>/remove-stock/",
        RemoveStockView.as_view(),
        name="inventory-remove-stock",
    ),
]
