from django.apps import AppConfig


class AdestisMaintenanceManagementAppConfig(AppConfig):
    name = 'adestis_netbox_maintenance_management'

    def ready(self):
        from .filtersets_extensions import register_filters
        register_filters()