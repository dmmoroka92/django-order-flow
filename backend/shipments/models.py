from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product


class Shipment(models.Model):
    class Status(models.TextChoices):
        DRAFT = ("draft", "Draft")
        CONFIRMED = ("confirmed", "Confirmed")
        SHIPPED = ("shipped", "Shipped")
        DELIVERED = ("delivered", "Delivered")
        CANCELLED = ("cancelled", "Cancelled")

    reference_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="shipments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_value(self) -> Decimal:
        return sum(
            (item.quantity * item.unit_price for item in self.shipment_items.all()),
            Decimal("0.00"),
        )

    def is_editable(self) -> bool:
        return self.status == self.Status.DRAFT

    def __str__(self) -> str:
        return f"Shipment {self.reference_number} ({self.status})"


class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="shipment_items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="shipment_items",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["shipment", "product"],
                name="unique_product_per_shipment",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="shipment_item_quantity_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gt=0),
                name="shipment_item_unit_price_positive",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.shipment.reference_number} - {self.product.sku} x {self.quantity}"
