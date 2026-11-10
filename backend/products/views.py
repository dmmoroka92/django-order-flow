from rest_framework import generics

from products.models import Product
from products.serializers import ProductSerializer


class ProductListView(generics.ListAPIView[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
