from django.urls import path

from shipments.views import ShipmentDetailView, ShipmentListCreateView

urlpatterns = [
    path("shipments/", ShipmentListCreateView.as_view(), name="shipment-list"),
    path("shipments/<int:pk>/", ShipmentDetailView.as_view(), name="shipment-detail"),
]
