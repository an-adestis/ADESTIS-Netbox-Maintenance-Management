from netbox.plugins import PluginConfig
from core.choices import JobIntervalChoices
class AdestisMaintenanceConfig(PluginConfig):
    name = 'adestis_netbox_maintenance_management'
    verbose_name = 'Maintenance'
    description = 'A NetBox plugin for managing maintenance.'
    version = '1.0.2'
    author = 'ADESTIS GmbH'
    author_email = 'pypi@adestis.de'
    base_url = 'maintenance'
    required_settings = []
    default_settings = {
        'top_level_menu' : True,
    }

    def ready(self):
        super().ready()
        from .jobs import AutoCreateMaintenanceTasks
        from .plan_jobs import AutoCreateMaintenancePlannedActions
        from .models import MaintenanceActions
        from .models import MaintenanceTasks
        
        # for obj in MaintenanceActions.objects.all():
        #     AutoCreateMaintenanceTasks.enqueue_once(
        #         instance=obj,
        #         interval=JobIntervalChoices.INTERVAL_MINUTELY
        #     )
            
        # for obj in MaintenanceTasks.objects.all():
        #     AutoCreateMaintenancePlannedActions.enqueue_once(
        #         instance=obj,
        #         interval=JobIntervalChoices.INTERVAL_MINUTELY
        #     )
        
config = AdestisMaintenanceConfig
default_app_config = "adestis_netbox_maintenance_management.apps.AdestisMaintenanceManagementAppConfig"


