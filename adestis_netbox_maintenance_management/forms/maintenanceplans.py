from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
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
from adestis_netbox_maintenance_management.models import MaintenancePlans

__all__ = (
    'MaintenancePlansForm',
    'MaintenancePlansFilterForm',
    'MaintenancePlansBulkEditForm',
    'MaintenancePlansCSVForm',
)


class MaintenancePlansForm(NetBoxModelForm):
    
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False
    )
    
    fieldsets = (
        FieldSet('name', 'reference_number', 'description', 'tags',  name=_('Maintenance Plans')),
        FieldSet('tenant', name=_("Tenant")),
    )
    
    class Meta:
        model = MaintenancePlans
        
        fields = ['name', 'reference_number', 'tenant', 'description', 'tags']
        
class MaintenancePlansBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=MaintenancePlans.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    reference_number = forms.IntegerField(
        required=False,
        label=_("Refrence Number")
    )
    
    comments = forms.CharField(
        max_length=150,
        required=False,
        label=_("Comment")
    )
    
    description = forms.CharField(
        max_length=500,
        required=False,
        label=_("Description"),
    )

    model = MaintenancePlans

    fieldsets = (
        FieldSet('name', 'reference_number', 'description', 'tags', name=_('Maintenance Plans')),
        FieldSet('tenant', name=_("Tenant")),
        
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description',
    ]
    
class MaintenancePlansFilterForm(NetBoxModelFilterSetForm):
    
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant')
    )
    
    model = MaintenancePlans

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'tag', 'reference_number', name=_('Maintenance Plans')),
        FieldSet('tenant_id', name=_("Tenant")),
        
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

class MaintenancePlansCSVForm(NetBoxModelImportForm):

    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned tenant')
    )
    
    class Meta:
        model = MaintenancePlans
        fields = ['name', 'tenant', 'reference_number', 'description', 'tags']
        default_return_url = 'plugins:adestis_netbox_maintenance_management:maintenanceplans_list'


