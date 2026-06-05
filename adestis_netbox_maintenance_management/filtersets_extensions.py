import django_filters
from virtualization.filtersets import VirtualMachineFilterSet
from dcim.filtersets import DeviceFilterSet
from tenancy.filtersets import TenantFilterSet
from adestis_netbox_maintenance_management.models import MaintenanceActions


def register_filters():
    vm_filter = django_filters.ModelMultipleChoiceFilter(
        field_name='maintenance_actions',
        queryset=MaintenanceActions.objects.all(),
    )
    VirtualMachineFilterSet.base_filters['maintenance_action_id'] = vm_filter
    VirtualMachineFilterSet.declared_filters['maintenance_action_id'] = vm_filter

    device_filter = django_filters.ModelMultipleChoiceFilter(
        field_name='maintenance_actions',
        queryset=MaintenanceActions.objects.all(),
    )
    DeviceFilterSet.base_filters['maintenance_action_id'] = device_filter
    DeviceFilterSet.declared_filters['maintenance_action_id'] = device_filter

    tenant_filter = django_filters.ModelMultipleChoiceFilter(
        field_name='action_tenant',
        queryset=MaintenanceActions.objects.all(),
    )
    TenantFilterSet.base_filters['maintenance_action_id'] = tenant_filter
    TenantFilterSet.declared_filters['maintenance_action_id'] = tenant_filter