from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.exceptions import InsufficientStockAPIError
from products.models import Inventory, Product
from products.serializers import (
    InventorySerializer,
    ProductSerializer,
    StockInventorySerializer,
)
from products.services.exceptions import InsufficientStockError
from products.services.stock_service import StockService

# PRODUCTS


class ProductListCreateView(generics.ListCreateAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# INVENTORY


class InventoryListCreateView(generics.ListCreateAPIView[Inventory]):
    queryset = Inventory.objects.select_related("product")
    serializer_class = InventorySerializer


class InventoryDetailView(generics.RetrieveAPIView[Inventory]):
    queryset = Inventory.objects.select_related("product")
    serializer_class = InventorySerializer


# STOCK MANAGEMENT


class RestockInventoryView(APIView):
    def post(self, request: Request, inventory_id: int) -> Response:
        serializer = StockInventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            StockService.restock(
                inventory_id=inventory_id,
                quantity=serializer.validated_data["quantity"],
            )
        except Inventory.DoesNotExist as exc:
            raise NotFound("Inventory not found") from exc

        return Response(status=status.HTTP_200_OK)


class RemoveStockView(APIView):
    def post(self, request: Request, inventory_id: int) -> Response:
        serializer = StockInventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            StockService.remove_stock(
                inventory_id=inventory_id,
                quantity=serializer.validated_data["quantity"],
            )
        except Inventory.DoesNotExist as exc:
            raise NotFound("Inventory not found") from exc
        except InsufficientStockError as exc:
            raise InsufficientStockAPIError(str(exc)) from exc

        return Response(status=status.HTTP_200_OK)
