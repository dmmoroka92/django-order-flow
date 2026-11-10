from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        error_messages={
            "blank": "Product name is required.",
            "max_length": "Product name must not exceed 255 characters.",
        },
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        error_messages={
            "blank": "SKU is required.",
            "unique": "A product with this SKU already exists.",
        },
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal(0.01),
                message="Unit price must be greater than zero.",
            )
        ],
        error_messages={
            "null": "Unit price is required.",
            "invalid": "Enter a valid unit price.",
        },
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} - ({self.sku})"
