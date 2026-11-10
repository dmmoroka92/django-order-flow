from rest_framework import serializers

from products.models import Inventory, Product


class ProductSerializer(serializers.ModelSerializer[Product]):
    class Meta:
        model = Product
        fields = "__all__"


class InventoryProductSerializer(serializers.ModelSerializer[Product]):
    class Meta:
        model = Product
        fields = ["id", "name", "sku"]


class InventorySerializer(serializers.ModelSerializer[Inventory]):
    product = InventoryProductSerializer(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        source="product",
        queryset=Product.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Inventory
        fields = ["id", "product", "product_id", "quantity", "updated_at"]
        read_only_fields = ["id", "updated_at"]


class StockInventorySerializer(serializers.Serializer[int]):
    quantity = serializers.IntegerField(min_value=0)
