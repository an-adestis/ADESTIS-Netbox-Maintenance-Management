from adestis_netbox_maintenance_management.models import MaintenanceWindows
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
    'MaintenanceWindowsFilterSet',
)

class MaintenanceWindowsFilterSet(NetBoxModelFilterSet):
    
    class Meta:
        model = MaintenanceWindows
        fields = ['id', 'name', 'schedule_type', 'start_time', 'end_time', 'recurrence_type', 'weekdays', 'monthdays', 'time', 'special_ordinal']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

