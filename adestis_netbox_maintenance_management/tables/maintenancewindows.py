from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceWindows
from adestis_netbox_maintenance_management.filtersets import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables

class MaintenanceWindowsTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()

    class Meta(NetBoxTable.Meta):
        model = MaintenanceWindows
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal', 'virtual_machine']
        default_columns = [ 'name', 'schedule_type' ]
        
    
    
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
            'pk', 'id', 'name', 'status', 'tenant_group', 'actions', 'maintenance_window', 'schedule_type'
        ]
        default_columns = [
            'pk', 'name', 'schedule_type'
        ]