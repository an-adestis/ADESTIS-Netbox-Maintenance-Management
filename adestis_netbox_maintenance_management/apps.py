from django.apps import AppConfig

class AdestisMaintenanceManagementAppConfig(AppConfig):
    name = 'adestis_netbox_maintenance_management'

    def ready(self):
        from adestis_netbox_maintenance_management.jobs import AutoCreateMaintenanceTasks
        from adestis_netbox_maintenance_management.plan_jobs import (
            AutoCreateMaintenancePlannedActions,
        )

