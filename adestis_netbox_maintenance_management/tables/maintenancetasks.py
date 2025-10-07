from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceTasks
from adestis_netbox_maintenance_management.filtersets import *
from dcim.models import *
from dcim.tables import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
class MaintenanceTasksTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    virtual_machine = tables.Column(
        linkify=True
    )
        
    maintenance_action = tables.Column(
        linkify= True
    )
    
    maintenance_windows = tables.Column(
        linkify= True
    )

    class Meta(NetBoxTable.Meta):

        model = MaintenanceTasks
        
        fields = ['name', 'maintenance_action', 'maintenance_windows', 'virtual_machine', 'description', 'tags', 'comments']
        default_columns = [ 'name', 'maintenance_windows', 'maintenance_action', 'virtual_machine', 'comments']


        