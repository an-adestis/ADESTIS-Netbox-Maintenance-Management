from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceActions
from adestis_netbox_maintenance_management.filtersets import *
from dcim.models import *
from dcim.tables import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
class MaintenanceActionsTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    device = tables.Column(
        linkify=True
    )
    
    virtual_machine = tables.Column(
        linkify=True
    )
        
    maintenance_window = tables.Column(
        linkify= True
    )

    class Meta(NetBoxTable.Meta):

        model = MaintenanceActions
        
        fields = ['name', 'maintenance_window', 'virtual_machine', 'device', 'description', 'tags', 'comments']
        default_columns = [ 'name', 'maintenance_window', 'device', 'virtual_machine']

class MaintenanceActionsTableTab(MaintenanceActionsTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    device = tables.Column(
        linkify=True
    )
    
    virtual_machine = tables.Column(
        linkify=True
    )
    
    class Meta(MaintenanceActionsTable.Meta):
        fields = ['name', 'maintenance_window', 'virtual_machine', 'device', 'description', 'tags', 'comments', 'actions']
        default_columns = [ 'name', 'maintenance_window', 'device', 'virtual_machine']
       
class DeviceTableMaintenanceActions(DeviceTable):
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(DeviceTable.Meta):  
        fields = (
            'pk', 'id', 'name', 'status', 'tenant', 'role', 'manufacturer', 'device_type',
            'serial', 'asset_tag', 'region', 'site_group', 'site', 'location', 'rack', 'parent_device',
            'device_bay_position', 'position', 'face', 'latitude', 'longitude', 'airflow', 'primary_ip', 'primary_ip4',
            'primary_ip6', 'oob_ip', 'cluster', 'virtual_chassis', 'vc_position', 'vc_priority', 'description',
            'config_template', 'comments', 'contacts', 'tags', 'created', 'last_updated', 'actions',
        )
        default_columns = (
            'pk', 'name', 'status', 'tenant', 'site', 'location', 'rack', 'role', 'manufacturer', 'device_type',
            'primary_ip',
        ) 
        
class VirtualMachineTableMaintenanceActions(VirtualMachineTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    class Meta(VirtualMachineTable.Meta):
        fields = [
            'pk', 'id', 'name', 'status', 'site', 'cluster', 'device', 'role', 'tenant', 'vcpus',
            'memory', 'disk', 'primary_ip4', 'primary_ip6', 'primary_ip', 'description', 'comments', 'config_template',
            'serial', 'contacts', 'tags', 'created', 'last_updated', 'actions',
        ]
        default_columns = [
            'pk', 'name', 'status', 'site', 'cluster', 'role', 'tenant', 'vcpus', 'memory', 'disk', 'primary_ip',
        ]
        
class DeviceTableMaintenanceActions(DeviceTable):
    
    actions = columns.ActionsColumn(
        actions=('edit',),
    )
    
    maintenance_actions = tables.Column(
        linkify= True
    )
    
    class Meta(DeviceTable.Meta):
        fields = (
            'pk', 'id', 'name', 'status', 'tenant', 'tenant_group', 'role', 'manufacturer', 'device_type',
            'serial', 'asset_tag', 'region', 'site_group', 'site', 'location', 'rack', 'parent_device',
            'device_bay_position', 'position', 'face', 'latitude', 'longitude', 'airflow', 'primary_ip', 'primary_ip4',
            'primary_ip6', 'oob_ip', 'cluster', 'virtual_chassis', 'vc_position', 'vc_priority', 'description',
            'config_template', 'comments', 'contacts', 'tags', 'created', 'last_updated', 'actions', 'maintenance_actions'
        )
        default_columns = (
            'pk', 'name', 'maintenance_actions'
        )