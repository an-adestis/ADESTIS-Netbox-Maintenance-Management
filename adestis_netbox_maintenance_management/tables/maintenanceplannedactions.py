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

class MaintenancePlannedActionsTable(NetBoxTable):
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
        linkify_item = True
    )
    
    maintenance_tasks = columns.ManyToManyColumn(
        linkify_item = True
    )
    
    maintenance_windows = columns.ManyToManyColumn(
        linkify_item = True
    )
    
    virtual_machine = columns.ManyToManyColumn(
        linkify_item = True
    )
    
    device = columns.ManyToManyColumn(
        linkify_item = True
    )
    
    pdf = tables.TemplateColumn(
        template_code="""
        <a href="{% url 'plugins:adestis_netbox_maintenance_management:export_planned_action_pdf' record.pk %}"
           class="btn btn-sm btn-primary">
           PDF
        </a>
        """,
        orderable=False
    )

    class Meta(NetBoxTable.Meta):

        model = MaintenancePlannedActions
        
        fields = ['name', 'maintenance_action', 'maintenance_tasks', 'maintenance_windows', 'virtual_machine', 'device', 'tenant', 'description', 'tags', 'comments', 'pdf']
        default_columns = [ 'name', 'tenant', 'maintenance_tasks', 'maintenance_windows', 'maintenance_action', 'virtual_machine', 'device', 'pdf']
        
    def render_pdf(self, record):
        url = reverse(
            "plugins:adestis_netbox_maintenance_management:export_planned_action_pdf",
            args=[record.pk],
        )
        return mark_safe(f'<a class="btn btn-sm btn-primary" href="{url}">PDF</a>')