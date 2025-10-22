from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceWindows
from adestis_netbox_maintenance_management.filtersets import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.safestring import mark_safe

def render_cron_value(obj):
    cron_value = obj.schedule_type.strip()
    return mark_safe(f'<span class="cron-expression">{cron_value}</span>')

class MaintenanceWindowsTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )
    
    virtual_machine = columns.ManyToManyColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    special_ordinal = columns.TemplateColumn(
         template_code="""
            <span class="cron-expression" title="{{ record.special_ordinal }}">{{ record.special_ordinal }}</span>
        """,
        verbose_name="Special Ordinal"
    )

    class Meta(NetBoxTable.Meta):
        model = MaintenanceWindows
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal', 'virtual_machine']
        default_columns = [ 'name', 'schedule_type', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal', 'virtual_machine']
        
class MaintenanceWindowsTableTab(MaintenanceWindowsTable):   
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(MaintenanceWindowsTable.Meta):
        model = MaintenanceWindows
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal', 'actions']
        default_columns = [ 'name', 'schedule_type', 'actions' ]
        
class VirtualMachineTableMaintenanceWindows(VirtualMachineTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    maintenance_window = tables.Column(
        linkify= True
    )
    
    class Meta(VirtualMachineTable.Meta):
        fields = [
            'pk', 'id', 'name', 'status', 'actions', 'maintenance_window', 'schedule_type'
        ]
        default_columns = [
            'pk', 'name', 'schedule_type'
        ]