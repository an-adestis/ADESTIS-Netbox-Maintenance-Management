from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceReport
from adestis_netbox_maintenance_management.filtersets import *
from dcim.models import *
from dcim.tables import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
class MaintenanceReportsTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()

        
    maintenance_planned_actions = tables.Column(
        linkify= True
    )

    class Meta(NetBoxTable.Meta):

        model = MaintenanceReport
        
        fields = ['name', 'maintenance_planned_actions', 'description', 'tags', 'comments']
        default_columns = [ 'name', 'maintenance_planned_actions', ]


        