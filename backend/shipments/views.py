from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer

from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer


class ShipmentListCreateView(generics.ListCreateAPIView[Shipment]):
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer

    def get_queryset(self) -> QuerySet[Shipment]:
        return (
            Shipment.objects.select_related("created_by")
            .prefetch_related("shipment_items__product")
            .order_by("-created_at")
        )

    def perform_create(self, serializer: BaseSerializer[Shipment]) -> None:
        serializer.save(created_by=self.request.user)


class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView[Shipment]):
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer

    def get_queryset(self) -> QuerySet[Shipment]:
        return Shipment.objects.select_related("created_by").prefetch_related(
            "shipment_items__product"
        )

    def perform_update(self, serializer: BaseSerializer[Shipment]) -> None:
        instance = serializer.instance

        if instance is None:
            raise ValidationError("Shipment instance is required.")

        if not instance.is_editable():
            raise ValidationError("Only draft shipments can be updated.")

        serializer.save()

    def perform_destroy(self, instance: Shipment) -> None:
        if not instance.is_editable():
            raise ValidationError("Only draft shipments can be deleted.")

        instance.delete()
