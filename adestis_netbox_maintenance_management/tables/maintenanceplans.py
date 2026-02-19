from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from dcim.models import *
from dcim.tables import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
from django.urls import reverse
from django.utils.safestring import mark_safe
class MaintenancePlansTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )
    
    maintenance_action = tables.Column(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    device = columns.ManyToManyColumn(
        linkify=True
    )
    
    virtual_machine = columns.ManyToManyColumn(
        linkify=True
    )
    
    tenant = tables.Column(
        linkify=True
    )
    
    reference_number = tables.Column()
    
    class Meta(NetBoxTable.Meta):

        model = MaintenancePlans
        
        fields = ['name',  'tenant', 'maintenance_actions', 'virtual_machine', 'device', 'reference_number', 'description', 'tags', 'comments', 'version']
        default_columns = [ 'name', 'maintenance_actions', 'tenant', 'virtual_machine', 'device', 'reference_number', 'version' ]
        


        