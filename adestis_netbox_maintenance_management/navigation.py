from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton
from netbox.choices import ButtonColorChoices
from django.conf import settings
from django.utils.translation import gettext_lazy as _


maintenance_windows_item = PluginMenuItem(
    link='plugins:adestis_netbox_maintenance_management:maintenancewindows_list',
    link_text=_('Maintenance Windows'),
    permissions=["adestis_netbox_maintenance_management.view_maintenancewindows"],
    buttons=(
        PluginMenuButton(
            link='plugins:adestis_netbox_maintenance_management:maintenancewindows_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["adestis_netbox_maintenance_management.add_maintenancewindows"]
        ),
    )
)

maintenance_actions_item = PluginMenuItem(
    link='plugins:adestis_netbox_maintenance_management:maintenanceactions_list',
    link_text=_('Maintenance Actions'),
    permissions=["adestis_netbox_maintenance_management.view_maintenanceactions"],
    buttons=(
        PluginMenuButton(
            link='plugins:adestis_netbox_maintenance_management:maintenanceactions_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["adestis_netbox_maintenance_management.add_maintenanceactions"]
        ),
    )
)

maintenance_planned_actions_item = PluginMenuItem(
    link='plugins:adestis_netbox_maintenance_management:maintenanceplannedactions_list',
    link_text=_('Planned Actions'),
    permissions=["adestis_netbox_maintenance_management.view_maintenanceplannedactions"],
)

maintenance_plans_item = PluginMenuItem(
    link='plugins:adestis_netbox_maintenance_management:maintenanceplans_list',
    link_text=_('Maintenance Plans'),
    permissions=["adestis_netbox_maintenance_management.view_maintenanceplans"],
    buttons=(
        PluginMenuButton(
            link='plugins:adestis_netbox_maintenance_management:maintenanceplans_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["adestis_netbox_maintenance_management.add_maintenanceplans"]
        ),
    )
)

maintenance_tasks_item = PluginMenuItem(
    link='plugins:adestis_netbox_maintenance_management:maintenancetasks_list',
    link_text=_('Maintenance Tasks'),
    permissions=["adestis_netbox_maintenance_management.view_maintenancetasks"],
    buttons=(
        PluginMenuButton(
            link='plugins:adestis_netbox_maintenance_management:maintenancetasks_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["adestis_netbox_maintenance_management.add_maintenancetasks"]
        ),
    )
)

maintenance_reports_item = PluginMenuItem(
    link='plugins:adestis_netbox_maintenance_management:maintenancereport_list',
    link_text=_('Maintenance Reports'),
    permissions=["adestis_netbox_maintenance_management.view_maintenancereport"],
    buttons=(
        PluginMenuButton(
            link='plugins:adestis_netbox_maintenance_management:maintenancereport_add',
            title=_('Add'),
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=["adestis_netbox_maintenance_management.add_maintenancereport"]
        ),
    )
)

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_maintenance_management', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(
        label="Maintenance",
        icon_class="mdi mdi-wrench",
        groups=[
            (
                _("Setup / Administration"),
                (
                    maintenance_windows_item,
                    maintenance_actions_item,
                    maintenance_plans_item,
                )
            ),
            (
                _("Operations"),
                (
                    maintenance_planned_actions_item,
                    maintenance_tasks_item, 
                )
            )
        ]
    )
else:
    menu_items = (
        maintenance_windows_item,
        maintenance_actions_item,
        maintenance_planned_actions_item,
        maintenance_tasks_item,
    )
