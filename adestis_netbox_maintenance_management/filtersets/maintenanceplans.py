from adestis_netbox_maintenance_management.models import MaintenanceActions
from adestis_netbox_maintenance_management.models import MaintenancePlans
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
    'MaintenancePlansFilterSet',
)

class MaintenancePlansFilterSet(NetBoxModelFilterSet):
    
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label=_('Tenant (ID)'),
    )
    
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        required=False,
        field_name='tenant__name',
        to_field_name='tenant',
        label=_('Tenant (name)'),
    )
    
    maintenance_action = django_filters.ModelMultipleChoiceFilter(
        queryset=MaintenanceActions.objects.all(),
        required = False,
        field_name='maintenance_action',
        label=_('Maintenance Action (name)'),
    )
    
    class Meta:
        model = MaintenancePlans
        fields = ['id', 'name', 'maintenance_action', 'tenant']
    

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

