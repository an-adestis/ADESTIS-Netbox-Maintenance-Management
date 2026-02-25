from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceWindows
from adestis_netbox_maintenance_management.filtersets import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
from django.utils.safestring import mark_safe
from cron_descriptor import get_description


def render_cron_value(obj):
    special = (getattr(obj, "special_ordinal", "") or "").strip()
    schedule = (getattr(obj, "schedule_type", "") or "").strip()

    if special:
        try:
            description = get_description(special)
            value = f"cron {description}"
        except Exception:
            value = f"cron {special}"
    else:
        value = schedule

    return mark_safe(
        f'<span class="cron-expression" title="{value}">{value}</span>'
    )

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
    
    special_ordinal = tables.Column(verbose_name="Special Ordinal")

    def render_special_ordinal(self, record):
        special = (record.special_ordinal or "").strip()

        if special:
            try:
                description = get_description(special)
                value = f"cron {description}"
            except Exception:
                value = f"cron {special}"
        else:
            value = "—"

        return mark_safe(
            f'<span class="cron-expression" title="{value}">{value}</span>'
        )

    class Meta(NetBoxTable.Meta):
        model = MaintenanceWindows
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'recurrence_type', 'weekdays', 'week_in_month', 'monthdays', 'day_of_month', 'special_ordinal', 'virtual_machine']
        default_columns = [ 'name', 'schedule_type', 'recurrence_type', 'weekdays', 'week_in_month', 'monthdays', 'day_of_month', 'special_ordinal', 'start_day', 'end_day', 'virtual_machine']
        
class MaintenanceWindowsTableTab(MaintenanceWindowsTable):   
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(MaintenanceWindowsTable.Meta):
        model = MaintenanceWindows
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'recurrence_type', 'weekdays', 'week_in_month', 'monthdays', 'day_of_month', 'special_ordinal', 'actions']
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