from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_maintenance_management.models.maintenancewindows import MaintenanceWindows, ScheduleTypeModeChoices, RecurrenceTypeChoices, Weekday
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CSVModelChoiceField,
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
from utilities.forms import ConfirmationForm

__all__ = (
    'MaintenanceWindowsForm',
    'MaintenanceWindowsFilterForm',
    'MaintenanceWindowsBulkEditForm',
    'MaintenanceWindowsCSVForm',
    
    'VirtualMachineFormAssignMaintenanceWindows',
    'VirtualMachineRemoveMaintenanceWindows',
)


class MaintenanceWindowsForm(NetBoxModelForm):
    
    fieldsets = (
        FieldSet('name', 'description', 'tags', 'schedule_type', 'start_time', 'end_time', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal', name=_('Maintenance Windows')),
    )
    
    class Meta:
        model = MaintenanceWindows
        
        fields = ['name', 'description', 'tags', 'comments',  
            'schedule_type',
            'start_time',
            'end_time',
            'recurrence_type',
            'weekdays',
            'monthdays', 
            'special_ordinal',
        ]
        
        widgets = {
            'start_time': DatePicker(),
            'end_time': DatePicker(),
            'monthdays': DatePicker(),
        }
        
        
class MaintenanceWindowsBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=MaintenanceWindows.objects.all(),
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
    
    schedule_type = forms.ChoiceField(
        label=_('Schedule Type'),
        choices=add_blank_choice(ScheduleTypeModeChoices),
        required=False,
        initial=''
    )

    model = MaintenanceWindows

    fieldsets = (
        FieldSet('name', 'description', 'tags', 'comments', 'schedule_type', 'start_time', 'end_time', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal', name=_('Maintenance Windows')),
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description',
    ]
    
class MaintenanceWindowsFilterForm(NetBoxModelFilterSetForm):
    
    model = MaintenanceWindows

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'tag', 'schedule_type',  name=_('Maintenanc Windows')),
        FieldSet('start_time', 'end_time', name=_("One Time")),
        FieldSet('recurrence_type', 'weekdays', 'monthdays', 'special_ordinal', name=_("Recurring"))
    )
    
    schedule_type = forms.MultipleChoiceField(
        required=False,
        choices=ScheduleTypeModeChoices
    )
    
    start_time = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    end_time = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    recurrence_type = forms.MultipleChoiceField(
        required=False,
        choices=RecurrenceTypeChoices
    )
    
    weekdays = forms.MultipleChoiceField(
        required = False,
        choices=Weekday
    )
    
    monthdays = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    special_ordinal = forms.CharField(
        required = False
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

class MaintenanceWindowsCSVForm(NetBoxModelImportForm):

    class Meta:
        model = MaintenanceWindows
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'start_time', 'end_time', 'recurrence_type', 'weekdays', 'monthdays', 'special_ordinal']
        default_return_url = 'plugins:adestis_netbox_maintenance_management:MaintenanceWindows_list'


class VirtualMachineFormAssignMaintenanceWindows(forms.Form):
    
    maintenance_window = DynamicModelMultipleChoiceField(
        label=_('Maintenance Windows'),
        queryset=MaintenanceWindows.objects.all()
    )

    class Meta:
        fields = [
            'maintenance_window',
        ]

    def __init__(self, virtual_machine, *args, **kwargs):

        self.virtual_machine = virtual_machine

        self.maintenance_window = DynamicModelMultipleChoiceField(
            label=_('Maintenance Windows'),
            queryset=MaintenanceWindows.objects.all()
        )        

        super().__init__(*args, **kwargs)

        self.fields['maintenance_window'].choices = []
        
class MaintenanceActionsRemoveVirtualMachine(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        widget=forms.MultipleHiddenInput()
    ) 
    
class VirtualMachineRemoveMaintenanceWindows(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=MaintenanceWindows.objects.all(),
        widget=forms.MultipleHiddenInput()
    ) 