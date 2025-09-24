from adestis_netbox_maintenance_management.models import MaintenanceActions
from netbox.filtersets import NetBoxModelFilterSet

from django.db.models import Q
from django.utils.translation import gettext as _

from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
)
import django_filters
from utilities.filters import TreeNodeMultipleChoiceFilter
from virtualization.models import *
from tenancy.models import *
from dcim.models import *
from ipam.api.serializers import *
from ipam.api.field_serializers import *
from adestis_netbox_maintenance_management.models import MaintenanceWindows

__all__ = (
    'MaintenanceActionsFilterSet',
)

class MaintenanceActionsFilterSet(NetBoxModelFilterSet):
    
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device',
        queryset=Device.objects.all()
    )
    
    virtual_machine_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualMachine.objects.all()
    )
    
    maintenance_window_id = django_filters.ModelMultipleChoiceFilter(
        queryset=MaintenanceWindows.objects.all(),
        label=_('Maintenance Window (ID)'),
    )
    
    maintenance_window = django_filters.ModelMultipleChoiceFilter(
        queryset=MaintenanceWindows.objects.all(),
        required = False,
        field_name='maintenance_window',
        label=_('Maintenance Window (name)'),
    )
    
    class Meta:
        model = MaintenanceActions
        fields = ['id', 'name', 'maintenance_window', 'device', 'virtual_machine_id']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

