from adestis_netbox_maintenance_management.models import MaintenanceActions, MaintenanceWindows
from adestis_netbox_maintenance_management.filtersets import *
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import MaintenanceActionsSerializer, MaintenanceWindowsSerializer

class MaintenanceWindowsViewSet(NetBoxModelViewSet):
    queryset = MaintenanceWindows.objects.prefetch_related(
        'tags'
    )
    serializer_class = MaintenanceWindowsSerializer
    filterset_class = MaintenanceWindowsFilterSet
    
class MaintenanceActionsViewSet(NetBoxModelViewSet):
    queryset = MaintenanceActions.objects.prefetch_related(
        'tags'
    )
    serializer_class = MaintenanceActionsSerializer
    filterset_class = MaintenanceActionsFilterSet