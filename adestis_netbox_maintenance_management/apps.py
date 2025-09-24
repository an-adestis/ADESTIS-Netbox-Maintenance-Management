from django.apps import AppConfig

class AdestisMaintenanceManagementAppConfig(AppConfig):
    name = 'adestis_netbox_certificate_management'

    def ready(self):
        from adestis_netbox_maintenance_management.jobs import AutoCreateMaintenancePlans

        AutoCreateMaintenancePlans.schedule(
            name="plan_metadata_extractor",
            interval=15  
        )
