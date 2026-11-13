from rest_framework import serializers

from shipments.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer[Shipment]):
    total_value = serializers.ReadOnlyField()
    is_editable = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = [
            "id",
            "reference_number",
            "status",
            "created_by",
            "total_value",
            "is_editable",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]
