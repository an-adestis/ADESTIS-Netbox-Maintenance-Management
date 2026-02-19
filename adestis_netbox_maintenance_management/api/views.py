from adestis_netbox_maintenance_management.models import MaintenanceActions, MaintenanceWindows, MaintenancePlannedActions, MaintenanceTasks, MaintenancePlans
from adestis_netbox_maintenance_management.filtersets import MaintenanceActionsFilterSet, MaintenanceWindowsFilterSet, MaintenancePlannedActionsFilterSet, MaintenanceTasksFilterSet, MaintenancePlansFilterSet
from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import MaintenanceActionsSerializer, MaintenanceWindowsSerializer, MaintenancePlannedActionsSerializer, MaintenanceTasksSerializer, MaintenancePlansSerializer

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
    
class MaintenancePlannedActionsViewSet(NetBoxModelViewSet):
    queryset = MaintenancePlannedActions.objects.prefetch_related(
        'tags'
    )
    serializer_class = MaintenancePlannedActionsSerializer
    filterset_class = MaintenancePlannedActionsFilterSet
    
class MaintenanceTasksViewSet(NetBoxModelViewSet):
    queryset = MaintenanceTasks.objects.prefetch_related(
        'tags'
    )
    serializer_class = MaintenanceTasksSerializer
    filterset_class = MaintenanceTasksFilterSet
    
class MaintenancePlansViewSet(NetBoxModelViewSet):
    queryset = MaintenancePlans.objects.prefetch_related(
        'tags'
    )
    serializer_class = MaintenancePlansSerializer
    filterset_class = MaintenancePlansFilterSet