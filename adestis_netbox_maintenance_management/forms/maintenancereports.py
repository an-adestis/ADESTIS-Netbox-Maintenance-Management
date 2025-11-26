from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_maintenance_management.models.maintenanceplannedactions import MaintenancePlannedActions
from utilities.forms import ConfirmationForm
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from tenancy.models import Tenant, TenantGroup
from dcim.models import *
from virtualization.models import *
from utilities.forms import BulkEditForm, add_blank_choice, form_from_model
from utilities.forms import get_field_value
from utilities.forms.widgets import DatePicker
from utilities.forms import get_field_value
from adestis_netbox_maintenance_management.models import MaintenanceReport

__all__ = (
    'MaintenanceReportsForm',
    'MaintenanceReportsFilterForm',
)


class MaintenanceReportsForm(NetBoxModelForm):
    
    
    
    fieldsets = (
        FieldSet('name', 'maintenance_planned_actions', name=_('Maintenance Reports')),
        
    )
    
    class Meta:
        model = MaintenanceReport
        
        fields = ['name', 'maintenance_planned_actions']
        
class MaintenanceReportsFilterForm(NetBoxModelFilterSetForm):
    
    
    
    maintenance_planned_actions_id = DynamicModelMultipleChoiceField(
        queryset=MaintenancePlannedActions.objects.all(),
        required=False,
        label=_('Planned Actions')
    )
    
    model = MaintenanceReport

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'maintenance_planned_actions_id', 'tag',  name=_('Maintenanc Planned Actions')),
    )