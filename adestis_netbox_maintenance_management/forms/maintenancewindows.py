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
from utilities.forms.widgets import DatePicker, TimePicker
from utilities.forms import get_field_value
from utilities.forms import ConfirmationForm

__all__ = (
    'MaintenanceWindowsForm',
    'MaintenanceWindowsFilterForm',
    'MaintenanceWindowsBulkEditForm',
    'MaintenanceWindowsCSVForm',
    
    # 'VirtualMachineFormAssignMaintenanceWindows',
    # 'VirtualMachineRemoveMaintenanceWindows',
)


class MaintenanceWindowsForm(NetBoxModelForm):
    
    
    fieldsets = (
        FieldSet('name', 'description', 'tags', 'start_time', 'end_time', 'schedule_type', 'start_day', 'end_day',  'recurrence_type', 'weekdays', 'monthdays', 'day_of_month', 'special_ordinal', 'week_in_month', name=_('Maintenance Windows')),
    )
    
    class Meta:
        model = MaintenanceWindows
        
        fields = ['name', 'description', 'tags', 'comments', 
            'start_time',
            'end_time', 
            'schedule_type',
            'start_day',
            'end_day',
            
            'recurrence_type',
            'weekdays',
            'monthdays', 
            'day_of_month',
            'special_ordinal',
            'week_in_month'
        ]
        
        widgets = {
            'start_day': DatePicker(),
            'end_day': DatePicker(),
            'start_time': TimePicker(),
            'end_time': TimePicker(),
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
        FieldSet('name', 'description', 'tags', 'comments', 'start_time', 'end_time', 'schedule_type', 'start_day', 'end_day',  'recurrence_type', 'weekdays', 'week_in_month', 'monthdays', 'day_of_month', 'special_ordinal', name=_('Maintenance Windows')),
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description',
    ]
    
class MaintenanceWindowsFilterForm(NetBoxModelFilterSetForm):
    
    model = MaintenanceWindows

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'tag', 'schedule_type',  name=_('Maintenanc Windows')),
        FieldSet('start_day', 'end_day', name=_("One Time")),
        FieldSet('recurrence_type', 'weekdays', 'week_in_month', 'monthdays', 'day_of_month', 'special_ordinal', name=_("Recurring")),
        FieldSet('start_time', 'end_time', name=_("Time"))
    )
    
    schedule_type = forms.MultipleChoiceField(
        required=False,
        choices=ScheduleTypeModeChoices
    )
    
    start_day = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    end_day = forms.DateField(
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
    
    day_of_month = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=31,
        label=_("Day of Month"),
        help_text=_("Specify the day of the month for monthly recurrence")
    )
    
    monthdays = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_("First Execution")
    )
    
    start_time = forms.TimeField(
        required = False
    )
    
    end_time = forms.TimeField(
        required = False
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
        fields = ['name', 'description', 'tags', 'comments', 'schedule_type', 'start_day', 'end_day', 'start_time', 'end_time', 'recurrence_type', 'weekdays', 'week_in_month', 'monthdays', 'day_of_month', 'special_ordinal']
        default_return_url = 'plugins:adestis_netbox_maintenance_management:MaintenanceWindows_list'
