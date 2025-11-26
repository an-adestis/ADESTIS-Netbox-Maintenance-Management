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
    
    refrence_number = tables.Column()

    class Meta(NetBoxTable.Meta):

        model = MaintenancePlans
        
        fields = ['name',  'tenant', 'refrence_number', 'description', 'tags', 'comments']
        default_columns = [ 'name', 'tenant', 'refrence_number' ]


        