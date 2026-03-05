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

from django.utils.html import format_html_join
from django.urls import reverse
class MaintenancePlansTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )
    
    maintenance_action = columns.ManyToManyColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    tenants = tables.Column(empty_values=())
    devices = tables.Column(empty_values=())
    virtual_machines = tables.Column(empty_values=())

    # ---------- TENANTS ----------
    
    reference_number = tables.Column()
    
    class Meta(NetBoxTable.Meta):

        model = MaintenancePlans
        
        fields = ['name',  'tenant', 'maintenance_action', 'virtual_machine', 'device', 'reference_number', 'description', 'tags', 'comments', 'version']
        default_columns = [ 'name', 'maintenance_action', 'tenant', 'virtual_machine', 'device', 'reference_number', 'version' ]

    def render_tenants(self, record):

        tenants = set()

        for action in record.maintenance_action.all():
            if action.tenant:
                tenants.add(action.tenant.name)

        return ", ".join(tenants)

    def render_devices(self, record):

        devices = []

        for action in record.maintenance_action.all():
            for device in action.device.all():
                devices.append(
                    f'<a href="{device.get_absolute_url()}">{device.name}</a>'
                )

        return tables.utils.mark_safe(", ".join(devices))

    def render_virtual_machines(self, record):

        vms = []

        for action in record.maintenance_action.all():
            for vm in action.virtual_machine.all():
                vms.append(
                    f'<a href="{vm.get_absolute_url()}">{vm.name}</a>'
                )

        return tables.utils.mark_safe(", ".join(vms))