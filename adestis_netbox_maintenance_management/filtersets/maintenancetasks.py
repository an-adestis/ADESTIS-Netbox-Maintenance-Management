from adestis_netbox_maintenance_management.models import MaintenanceActions, MaintenanceTasks, MaintenanceWindows
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


__all__ = (
    'MaintenanceTasksFilterSet',
)

class MaintenanceTasksFilterSet(NetBoxModelFilterSet):
    
    virtual_machine = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualMachine.objects.all()
    )
    
    maintenance_action = django_filters.ModelMultipleChoiceFilter(
        queryset=MaintenanceActions.objects.all()
    )
    
    maintenance_windows = django_filters.ModelMultipleChoiceFilter(
        queryset=MaintenanceWindows.objects.all()
    )
    
    class Meta:
        model = MaintenanceTasks
        fields = ['id', 'name', 'maintenance_action', 'maintenance_windows', 'virtual_machine']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

