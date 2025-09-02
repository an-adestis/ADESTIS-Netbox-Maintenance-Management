from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_maintenance_management.models.maintenanceactions import MaintenanceActions
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

__all__ = (
    'MaintenanceActionsForm',
    'MaintenanceActionsFilterForm',
    'MaintenanceActionsBulkEditForm',
    'MaintenanceActionsCSVForm',
)


class MaintenanceActionsForm(NetBoxModelForm):
    
    fieldsets = (
        FieldSet('name', 'description', 'tags',  name=_('Maintenance Actions')),
    )
    
    class Meta:
        model = MaintenanceActions
        
        fields = ['name', 'description', 'tags', 'comments']
        
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

    model = MaintenanceActions

    fieldsets = (
        FieldSet('name', 'description', 'tags', 'comments', name=_('Maintenance Windows')),
    )

    nullable_fields = [
        'add_tags', 'remove_tags', 'description',
    ]
    
class MaintenanceActionsFilterForm(NetBoxModelFilterSetForm):
    
    model = MaintenanceActions

    fieldsets = (
        FieldSet('q', 'index',),
        FieldSet('name', 'tag',  name=_('Maintenanc Windows')),
    )

    index = forms.IntegerField(
        required=False
    )

    tag = TagFilterField(model)

class MaintenanceActionsCSVForm(NetBoxModelImportForm):

    class Meta:
        model = MaintenanceActions
        fields = ['name', 'description', 'tags', 'comments']
        default_return_url = 'plugins:adestis_netbox_maintenance_management:MaintenanceActions_list'


    