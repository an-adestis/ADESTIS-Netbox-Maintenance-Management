from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceActions
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
        
    maintenance_action = tables.Column(
        linkify= True
    )

    class Meta(NetBoxTable.Meta):

        model = MaintenanceActions
        
        fields = ['name', 'maintenance_action', 'tenant', 'description', 'tags', 'comments']
        default_columns = [ 'name', 'tenant', 'maintenance_action']


        