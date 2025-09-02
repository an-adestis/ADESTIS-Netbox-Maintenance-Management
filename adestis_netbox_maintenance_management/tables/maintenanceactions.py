from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceActions
from adestis_netbox_maintenance_management.filtersets import *


class MaintenanceActionsTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()

    class Meta(NetBoxTable.Meta):
        model = MaintenanceActions
        fields = ['name', 'description', 'tags', 'comments']
        default_columns = [ 'name' ]
        