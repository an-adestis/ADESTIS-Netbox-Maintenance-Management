from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_maintenance_management.models.maintenanceactions import MaintenanceActions
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
        required=False,
        # query_params={
        #     'group_id': '$tenant_group'
        # },
    )
    
    fieldsets = (
        FieldSet('name', 'maintenance_action', 'description', 'tags',  name=_('Maintenance Plans')),
        FieldSet('tenant', name=_("Tenant")),
        
    )
    
    class Meta:
        model = MaintenancePlans
        
        fields = ['name', 'maintenance_action', 'tenant', 'description', 'tags', 'comments']
        
class MaintenancePlansBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=MaintenanceActions.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
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
    
    maintenance_action = DynamicModelChoiceField(
        queryset=MaintenanceActions.objects.all(),
        required= False,
        label=_('Maintenance Action'),
    )

    model = MaintenancePlans

    fieldsets = (
        FieldSet('name', 'maintenance_action', 'description', 'tags', 'comments', name=_('Maintenance Plans')),
        FieldSet('tenant', name=_("Tenant")),
        
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description',
    ]
    
class MaintenancePlansFilterForm(NetBoxModelFilterSetForm):
    
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        # query_params={
        #     'group_id': '$tenant_group_id'
        # },
        label=_('Tenant')
    )
    
    # maintenance_action_id = DynamicModelMultipleChoiceField(
    #     queryset=MaintenanceActions.objects.all(),
    #     required=False,
    #     label=_('Maintenance Actions')
    # )
    
    model = MaintenancePlans

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'tag',  name=_('Maintenanc Plans')),
        FieldSet('tenant_id', name=_("Tenant")),
        
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

class MaintenancePlansCSVForm(NetBoxModelImportForm):
    
    maintenance_action = CSVModelChoiceField(
        label=_('Maintenance Windows'),
        queryset=MaintenanceActions.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned maintenance window')
    )
    
    tenant = CSVModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned tenant')
    )
    
    class Meta:
        model = MaintenancePlans
        fields = ['name', 'maintenance_action', 'tenant', 'description', 'tags', 'comments']
        default_return_url = 'plugins:adestis_netbox_maintenance_management:MaintenanceActions_list'


