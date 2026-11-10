from rest_framework import generics

from products.models import Product
from products.serializers import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
