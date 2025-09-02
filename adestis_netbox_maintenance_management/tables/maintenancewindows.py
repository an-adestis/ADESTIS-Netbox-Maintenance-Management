from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceWindows
from adestis_netbox_maintenance_management.filtersets import *


class MaintenanceWindowsTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()

    class Meta(NetBoxTable.Meta):
        model = MaintenanceWindows
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal']
        default_columns = [ 'name', 'schedule_type' ]
        