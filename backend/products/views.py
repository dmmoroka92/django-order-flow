from rest_framework import generics

from products.models import Inventory, Product
from products.serializers import InventorySerializer, ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InventoryListCreateView(generics.ListCreateAPIView[Inventory]):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView[Inventory]):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
