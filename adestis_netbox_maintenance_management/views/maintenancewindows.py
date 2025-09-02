from netbox.views import generic
from adestis_netbox_maintenance_management.forms import *
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from adestis_netbox_maintenance_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect

__all__ = (
    'MaintenanceWindowsView',
    'MaintenanceWindowsListView',
    'MaintenanceWindowsEditView',
    'MaintenanceWindowsDeleteView',
    'MaintenanceWindowsBulkDeleteView',
    'MaintenanceWindowsBulkEditView',
    'MaintenanceWindowsBulkImportView',
)

class MaintenanceWindowsView(generic.ObjectView):
    queryset = MaintenanceWindows.objects.all()
    

class MaintenanceWindowsListView(generic.ObjectListView):
    queryset = MaintenanceWindows.objects.all()
    table = MaintenanceWindowsTable
    filterset = MaintenanceWindowsFilterSet
    filterset_form = MaintenanceWindowsFilterForm
    

class MaintenanceWindowsEditView(generic.ObjectEditView):
    queryset = MaintenanceWindows.objects.all()
    form = MaintenanceWindowsForm
    template_name = "adestis_netbox_maintenance_management/maintenancewindowsadd.html"


class MaintenanceWindowsDeleteView(generic.ObjectDeleteView):
    queryset = MaintenanceWindows.objects.all() 

class MaintenanceWindowsBulkDeleteView(generic.BulkDeleteView):
    queryset = MaintenanceWindows.objects.all()
    table = MaintenanceWindowsTable
    
    
class MaintenanceWindowsBulkEditView(generic.BulkEditView):
    queryset = MaintenanceWindows.objects.all()
    filterset = MaintenanceWindowsFilterSet
    table = MaintenanceWindowsTable
    form =  MaintenanceWindowsBulkEditForm
    

class MaintenanceWindowsBulkImportView(generic.BulkImportView):
    queryset = MaintenanceWindows.objects.all()
    model_form = MaintenanceWindowsCSVForm
    table = MaintenanceWindowsTable
    