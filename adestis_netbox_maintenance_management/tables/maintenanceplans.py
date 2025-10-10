from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from dcim.models import *
from dcim.tables import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
class MaintenancePlansTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    tenant = tables.Column(
        linkify=True
    )
        
    maintenance_action = columns.ManyToManyColumn(
        linkify = True
    )
    
    maintenance_tasks = columns.ManyToManyColumn(
        linkify = True
    )
    
    maintenance_windows = columns.ManyToManyColumn(
        linkify = True
    )
    
    virtual_machine = columns.ManyToManyColumn(
        linkify = True
    )
    
    device = columns.ManyToManyColumn(
        linkify = True
    )

    class Meta(NetBoxTable.Meta):

        model = MaintenancePlans
        
        fields = ['name', 'maintenance_action', 'maintenance_tasks', 'maintenance_windows', 'virtual_machine', 'device', 'tenant', 'description', 'tags', 'comments']
        default_columns = [ 'name', 'tenant', 'maintenance_tasks', 'maintenance_windows', 'maintenance_action', 'virtual_machine', 'device' ]


        