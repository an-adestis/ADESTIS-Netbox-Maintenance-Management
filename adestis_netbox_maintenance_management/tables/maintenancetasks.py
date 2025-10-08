from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceTasks, MaintenanceActions
from adestis_netbox_maintenance_management.filtersets import *
from dcim.models import *
from dcim.tables import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
from netbox.tables.columns import ManyToManyColumn 
from netbox.tables.columns import BooleanColumn
from django.utils.safestring import mark_safe
from netbox.tables.columns import TemplateColumn

class MaintenanceTasksTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    virtual_machine = columns.ManyToManyColumn(
        linkify= True,
        verbose_name="Virtual Machines"
    )
    
        
    maintenance_action = tables.Column(
        linkify= True
    )
    
    maintenance_windows = tables.Column(
        linkify= True
    )
    
    done = TemplateColumn(
        template_code="""
        <input type="checkbox"
            class="js-done-toggle"
            data-pk="{{ record.pk }}"
            onchange="localStorage.setItem('maintenance_done_{{ record.pk }}', this.checked ? '1' : '0')"
            {% if record.pk|stringformat:"s" in request.GET.localstorage_keys %}checked{% endif %}>
    """,
        verbose_name="Done",
        orderable=False
    )


    class Meta(NetBoxTable.Meta):

        model = MaintenanceTasks
        
        fields = ['name', 'maintenance_action', 'maintenance_windows', 'virtual_machine', 'description', 'tags', 'comments', 'done']
        default_columns = [ 'name', 'maintenance_windows', 'maintenance_action', 'virtual_machine', 'done', 'comments']


        