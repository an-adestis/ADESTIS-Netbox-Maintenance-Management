from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'adestis_netbox_maintenance_management'

router = NetBoxRouter()
router.register('maintenancewindows', views.MaintenanceWindowsViewSet)
router.register('maintenanceactions', views.MaintenanceActionsViewSet)
router.register('maintenanceplans', views.MaintenancePlansViewSet)
router.register('maintenancereports', views.MaintenanceReportsViewSet)
router.register('maintenancetasks', views.MaintenanceTasksViewSet)
urlpatterns = router.urls
