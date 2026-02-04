from django.apps import AppConfig

class AdestisMaintenanceManagementAppConfig(AppConfig):
    name = 'adestis_netbox_maintenance_management'

    def ready(self):
        from adestis_netbox_maintenance_management.jobs import AutoCreateMaintenanceTasks
        from adestis_netbox_maintenance_management.plan_jobs import (
            AutoCreateMaintenancePlannedActions,
        )

        
        AutoCreateMaintenanceTasks.schedule(
            name="auto_create_maintenance_tasks",
            interval=15,   
            overwrite=True,
        )

        
        AutoCreateMaintenancePlannedActions.schedule(
            name="auto_create_maintenance_planned_actions",
            interval=1,    
            overwrite=True,
        )
