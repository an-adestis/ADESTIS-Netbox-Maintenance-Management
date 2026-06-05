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
        from . import jobs
        from . import plan_jobs
        from .filtersets_extensions import register_filters
        register_filters()

        
config = AdestisMaintenanceConfig



