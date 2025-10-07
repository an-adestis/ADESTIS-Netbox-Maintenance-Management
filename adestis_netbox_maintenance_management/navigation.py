from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings

_maintenancewindows = [
    PluginMenuItem(
        link='plugins:adestis_netbox_maintenance_management:maintenancewindows_list',
        link_text='Maintenance Windows',
        permissions=["adestis_netbox_maintenance_management.maintenancewindows_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_maintenance_management:maintenancewindows_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_maintenance_management.maintenancewindows_add"]),
        )
    ),    
]

_maintenanceactions = [
    PluginMenuItem(
        link='plugins:adestis_netbox_maintenance_management:maintenanceactions_list',
        link_text='Maintenance Actions',
        permissions=["adestis_netbox_maintenance_management.maintenanceactions_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_maintenance_management:maintenanceactions_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_maintenance_management.maintenanceactions_add"]),
        )
    ),    
]

_maintenanceplans = [
    PluginMenuItem(
        link='plugins:adestis_netbox_maintenance_management:maintenanceplans_list',
        link_text='Maintenance Plans',
        permissions=["adestis_netbox_maintenance_management.maintenanceplans_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_maintenance_management:maintenanceplans_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_maintenance_management.maintenanceplans_add"]),
        )
    ),    
]

_maintenancereports = [
    PluginMenuItem(
        link='plugins:adestis_netbox_maintenance_management:maintenancereport_list',
        link_text='Maintenance Reports',
        permissions=["adestis_netbox_maintenance_management.maintenancereport_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_maintenance_management:maintenancereport_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_maintenance_management.maintenancereport_add"]),
        )
    ),    
]

_maintenancetasks = [
    PluginMenuItem(
        link='plugins:adestis_netbox_maintenance_management:maintenancetasks_list',
        link_text='Maintenance Tasks',
        permissions=["adestis_netbox_maintenance_management.maintenancetasks_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_maintenance_management:maintenancetasks_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_maintenance_management.maintenancetasks_add"]),
            
        )
    ),
]

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_maintenance_management', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="Maintenance",
        groups=(
            ("Maintenance Windows", _maintenancewindows),
            ("Maintenance Actions", _maintenanceactions),
            ("Maintenance Plans", _maintenanceplans),
            ("Maintenance Reports", _maintenancereports),
            ("Maintenance Tasks", _maintenancetasks),
        ),
        icon_class="mdi mdi-wrench",
    )
else:
    menu_items = _maintenancewindows