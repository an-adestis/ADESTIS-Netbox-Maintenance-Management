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

__all__ = (
    'MaintenanceActionsFilterSet',
)

class MaintenanceActionsFilterSet(NetBoxModelFilterSet):
    
    class Meta:
        model = MaintenanceActions
        fields = ['id', 'name']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

