from netbox.views import generic
from adestis_netbox_maintenance_management.forms.maintenanceactions import *
from adestis_netbox_maintenance_management.models.maintenanceactions import *
from adestis_netbox_maintenance_management.filtersets.maintenanceactions import *
from adestis_netbox_maintenance_management.tables.maintenanceactions import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect

__all__ = (
    'MaintenanceActionsView',
    'MaintenanceActionsListView',
    'MaintenanceActionsEditView',
    'MaintenanceActionsDeleteView',
    'MaintenanceActionsBulkDeleteView',
    'MaintenanceActionsBulkEditView',
    'MaintenanceActionsBulkImportView',
)

class MaintenanceActionsView(generic.ObjectView):
    queryset = MaintenanceActions.objects.all()
    

class MaintenanceActionsListView(generic.ObjectListView):
    queryset = MaintenanceActions.objects.all()
    table = MaintenanceActionsTable
    filterset = MaintenanceActionsFilterSet
    filterset_form = MaintenanceActionsFilterForm
    

class MaintenanceActionsEditView(generic.ObjectEditView):
    queryset = MaintenanceActions.objects.all()
    form = MaintenanceActionsForm
    # template_name = "adestis_netbox_maintenance_management/maintenanceactionsadd.html"


class MaintenanceActionsDeleteView(generic.ObjectDeleteView):
    queryset = MaintenanceActions.objects.all() 

class MaintenanceActionsBulkDeleteView(generic.BulkDeleteView):
    queryset = MaintenanceActions.objects.all()
    table = MaintenanceActionsTable
    
    
class MaintenanceActionsBulkEditView(generic.BulkEditView):
    queryset = MaintenanceActions.objects.all()
    filterset = MaintenanceActionsFilterSet
    table = MaintenanceActionsTable
    form =  MaintenanceActionsBulkEditForm
    

class MaintenanceActionsBulkImportView(generic.BulkImportView):
    queryset = MaintenanceActions.objects.all()
    model_form = MaintenanceActionsCSVForm
    table = MaintenanceActionsTable
    