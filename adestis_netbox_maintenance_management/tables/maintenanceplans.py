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

    description = columns.MarkdownColumn()
    
    tenant = tables.Column(
        linkify=True
    )
    
    refrence_number = tables.Column()
    
    pdf = tables.Column(empty_values=(), verbose_name="PDF", orderable=False)

    class Meta(NetBoxTable.Meta):

        model = MaintenancePlans
        
        fields = ['name',  'tenant', 'refrence_number', 'description', 'tags', 'comments', 'pdf']
        default_columns = [ 'name', 'tenant', 'refrence_number', 'pdf' ]
        
    def render_pdf(self, record):
        url = reverse(
            "plugins:adestis_netbox_maintenance_management:export_pdf",
            args=[record.pk],
        )
        return mark_safe(f'<a class="btn btn-sm btn-primary" href="{url}">PDF</a>')


        