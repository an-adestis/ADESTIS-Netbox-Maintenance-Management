from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_maintenance_management.models import *
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


__all__ = (
    'MaintenanceTasksForm',
    'MaintenanceTasksFilterForm',
    'MaintenanceTasksBulkEditForm',
    'MaintenanceTasksCSVForm',
)


class MaintenanceTasksForm(NetBoxModelForm):
    
    fieldsets = (
        FieldSet('name', 'status', 'maintenance_action', 'maintenance_windows', 'description', 'tags',  name=_('Maintenance Tasks')),
        FieldSet('virtual_machine', name=_("Virtual Machine")),
        FieldSet('device', name=_("Device")),
    )
    
    class Meta:
        model = MaintenanceTasks
        
        fields = ['name', 'status', 'maintenance_action', 'maintenance_windows', 'virtual_machine', 'device', 'description', 'tags', 'comments']
        
class MaintenanceTasksBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=MaintenanceActions.objects.all(),
        widget=forms.MultipleHiddenInput, 
    )
    
    name = forms.CharField(
        required=False,
        max_length = 150,
        label=_("Name"),
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=TaskStatusChoices,
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
    
    maintenance_windows = DynamicModelChoiceField(
        queryset=MaintenanceWindows.objects.all(),
        required= False,
        label=_('Maintenance Window'),
    )
    
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required= False,
        label=_('Virtual Machine'),
    )
    
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required= False,
        label=_('Device'),
    )

    model = MaintenanceTasks

    fieldsets = (
        FieldSet('name', 'status', 'maintenance_action', 'maintenance_windows', 'description', 'tags', 'comments', name=_('Maintenance Tasks')),
        FieldSet('virtual_machine', name=_("Virtual Machine")),
        FieldSet('device', name=_("Device")),
        
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description',
    ]
    
class MaintenanceTasksFilterForm(NetBoxModelFilterSetForm):
    
    status = forms.MultipleChoiceField(
        choices=TaskStatusChoices,
        required=False,
        label=_('Status')
    )
    
    maintenance_windows = DynamicModelMultipleChoiceField(
        queryset=MaintenanceActions.objects.all(),
        required=False,
        label=_('Maintenance Actions')
    )
    
    maintenance_action = DynamicModelMultipleChoiceField(
        queryset=MaintenanceActions.objects.all(),
        required=False,
        label=_('Maintenance Actions')
    )
    
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        label=_('Virtual Machine'),
        required=False,
    )
    
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        label=_('Device'),
        required=False,
    )
    
    model = MaintenanceTasks

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'status', 'tag', 'maintenance_action', 'maintenance_windows', name=_('Maintenance Tasks')),
        FieldSet('virtual_machine', name=_("Virtual Machine")), 
        FieldSet('device', name=_("Device")), 
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

class MaintenanceTasksCSVForm(NetBoxModelImportForm):
    
    status = CSVChoiceField(
        choices=TaskStatusChoices,
        help_text=_('Status'),
        required=True,
    )
    
    maintenance_action = CSVModelChoiceField(
        label=_('Maintenance Windows'),
        queryset=MaintenanceActions.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned maintenance action')
    )
    
    maintenance_windows = CSVModelChoiceField(
        label=_('Maintenance Windows'),
        queryset=MaintenanceWindows.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned maintenance window')
    )
    
    virtual_machine = CSVModelMultipleChoiceField(
        label=_('Virtual Machines'),
        queryset=VirtualMachine.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned virtual machine')
    )
    
    device = CSVModelMultipleChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned device')
    )
    
    class Meta:
        model = MaintenanceTasks
        fields = ['name', 'status', 'maintenance_action', 'virtual_machine', 'device', 'description', 'tags', 'comments']
        default_return_url = 'plugins:adestis_netbox_maintenance_management:MaintenanceActions_list'


