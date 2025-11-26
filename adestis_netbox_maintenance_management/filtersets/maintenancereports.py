from adestis_netbox_maintenance_management.models import MaintenanceActions
from adestis_netbox_maintenance_management.models import MaintenancePlannedActions
from adestis_netbox_maintenance_management.models import MaintenanceReport
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
    'MaintenanceReportsFilterSet',
)

class MaintenanceReportsFilterSet(NetBoxModelFilterSet):
    
    maintenance_planned_actions_id = django_filters.ModelMultipleChoiceFilter(
        queryset=MaintenancePlannedActions.objects.all(),
        label=_('Planned Actions (ID)'),
    )
    
    maintenance_planned_actions = django_filters.ModelMultipleChoiceFilter(
        queryset=MaintenancePlannedActions.objects.all(),
        required = False,
        field_name='maintenance_planned_actions',
        label=_('Maintenance  (name)'),
    )
    
    class Meta:
        model = MaintenanceReport
        fields = ['id', 'maintenance_planned_actions', 'name']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset