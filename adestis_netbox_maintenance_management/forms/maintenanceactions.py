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
from adestis_netbox_maintenance_management.models import MaintenanceWindows

__all__ = (
    'MaintenanceActionsForm',
    'MaintenanceActionsFilterForm',
    'MaintenanceActionsBulkEditForm',
    'MaintenanceActionsCSVForm',
    
    
    'MaintenanceActionsAssignDeviceForm',
    'MaintenanceActionsRemoveDevice',
    
    'MaintenanceActionsAssignVirtualMachineForm',
    'MaintenanceActionsRemoveVirtualMachine',
    
    'DeviceFormAssignMaintenanceAction',
    'VirtualMachineFormAssignMaintenanceAction',
    
    'VirtualMachineRemoveMaintenanceActions',
    'DeviceRemoveMaintenanceActions',
    
)


class MaintenanceActionsForm(NetBoxModelForm):
    
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'cluster_id': '$cluster',
        },
        help_text=_("Device"),
    )
    
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'cluster_id': '$cluster',
            'device_id': '$device',
        },
        help_text=_("Virtual Machine"),
    )
    
    fieldsets = (
        FieldSet('name', 'maintenance_window', 'description', 'tags',  name=_('Maintenance Actions')),
        FieldSet('device', name=_("Device")),
        FieldSet('virtual_machine', name=_("Virtual Machine")),
    )
    
    class Meta:
        model = MaintenanceActions
        
        fields = ['name', 'maintenance_window', 'device', 'virtual_machine', 'description', 'tags', 'comments']
        
class MaintenanceActionsBulkEditForm(NetBoxModelBulkEditForm):
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
    
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required = False,
        label = ("Virtual Machines"),
        null_option='None'
    )

    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required = False,
        label =_("Devices"),
        null_option='None'
    )
    
    maintenance_window = DynamicModelChoiceField(
        queryset=MaintenanceWindows.objects.all(),
        required= False,
        label=_('Maintenance Window'),
    )

    model = MaintenanceActions

    fieldsets = (
        FieldSet('name', 'maintenance_window', 'description', 'tags', 'comments', name=_('Maintenance Actions')),
        FieldSet('device', name=_("Device")),
        FieldSet('virtual_machine', name=_("Virtual Machine")),
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description',
    ]
    
class MaintenanceActionsFilterForm(NetBoxModelFilterSetForm):
    
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
    
    maintenance_window_id = DynamicModelMultipleChoiceField(
        queryset=MaintenanceWindows.objects.all(),
        required=False,
        label=_('Maintenance Windows')
    )
    
    model = MaintenanceActions

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'maintenance_window_id', 'tag',  name=_('Maintenanc Actions')),
        FieldSet('device', name=_("Device")),
        FieldSet('virtual_machine', name=_("Virtue Machine")),
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

class MaintenanceActionsCSVForm(NetBoxModelImportForm):

    virtual_machine = CSVModelMultipleChoiceField(
        label=_('Virtual Machines'),
        queryset=VirtualMachine.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned virtual machine')
    )
    
    device = CSVModelMultipleChoiceField(
        label=_('Devices'),
        queryset=Device.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned device')
    )
    
    maintenance_window = CSVModelChoiceField(
        label=_('Maintenance Windows'),
        queryset=MaintenanceWindows.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Name of assigned maintenance window')
    )
    
    class Meta:
        model = MaintenanceActions
        fields = ['name', 'maintenance_window', 'device', 'virtual_machine', 'description', 'tags', 'comments']
        default_return_url = 'plugins:adestis_netbox_maintenance_management:MaintenanceActions_list'


class MaintenanceActionsAssignDeviceForm(forms.Form):
    
    device = DynamicModelMultipleChoiceField(
        label=_('Devices'),
        queryset=Device.objects.all()
    )

    class Meta:
        fields = [
            'device',
        ]

    def __init__(self, maintenance_actions,*args, **kwargs):

        self.maintenance_actions = maintenance_actions

        self.device = DynamicModelMultipleChoiceField(
            label=_('Devices'),
            queryset=Device.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['device'].choices = []
        
class MaintenanceActionsAssignVirtualMachineForm(forms.Form):
    
    virtual_machine = DynamicModelMultipleChoiceField(
        label=_('Virtual Machines'),
        queryset=VirtualMachine.objects.all()
    )

    class Meta:
        fields = [
            'virtual_machine',
        ]

    def __init__(self, maintenance_actions,*args, **kwargs):

        self.maintenance_actions = maintenance_actions

        self.virtual_machine = DynamicModelMultipleChoiceField(
            label=_('Virtual Machines'),
            queryset=VirtualMachine.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['virtual_machine'].choices = []

class DeviceFormAssignMaintenanceAction(forms.Form):
    
    maintenance_actions = DynamicModelMultipleChoiceField(
        label=_('Maintenance Actions'),
        queryset=MaintenanceActions.objects.all()
    )
    
    def __init__(self, *args, **kwargs):
        self.device = kwargs.pop('device', None)
        super().__init__(*args, **kwargs)

    class Meta:
        fields = [
            'maintenance_actions'
        ]
        
    def _init_(self, device, *args, **kwargs):
        
        self.device = device
        
        self.device = DynamicModelMultipleChoiceField(
            label=_('Maintenance Actions'),
            queryset=MaintenanceActions.objects.all()
        )

        super().__init__(*args, **kwargs)
        
        self.fields['maintenance_actions'].choices = []
        
class VirtualMachineFormAssignMaintenanceAction(forms.Form):
    
    maintenance_actions = DynamicModelMultipleChoiceField(
        label=_('Maintenance Actions'),
        queryset=MaintenanceActions.objects.all()
    )
    
    def __init__(self, *args, **kwargs):
        self.virtual_machine = kwargs.pop('virtual_machine', None)
        super().__init__(*args, **kwargs)

    class Meta:
        fields = [
            'maintenance_actions'
        ]
        
    def _init_(self, virtual_machine, *args, **kwargs):
        
        self.virtual_machine = virtual_machine
        
        self.virtual_machine = DynamicModelMultipleChoiceField(
            label=_('Maintenance Actions'),
            queryset=MaintenanceActions.objects.all()
        )

        super().__init__(*args, **kwargs)
        
        self.fields['maintenance_actions'].choices = []
        
class MaintenanceActionsRemoveDevice(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Device.objects.all(),
        widget=forms.MultipleHiddenInput()
    ) 
    
class MaintenanceActionsRemoveVirtualMachine(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        widget=forms.MultipleHiddenInput()
    ) 
    
class VirtualMachineRemoveMaintenanceActions(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=MaintenanceActions.objects.all(),
        widget=forms.MultipleHiddenInput()
    ) 
    
class DeviceRemoveMaintenanceActions(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=MaintenanceActions.objects.all(),
        widget=forms.MultipleHiddenInput()
    ) 