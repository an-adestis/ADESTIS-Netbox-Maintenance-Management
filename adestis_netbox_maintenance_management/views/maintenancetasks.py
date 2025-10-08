from netbox.views import generic
from adestis_netbox_maintenance_management.forms import *
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from adestis_netbox_maintenance_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse

__all__ = (
    'MaintenanceTasksView',
    'MaintenanceTasksListView',
    'MaintenanceTasksEditView',
    'MaintenanceTasksDeleteView',
    'MaintenanceTasksBulkDeleteView',
    'MaintenanceTasksBulkEditView',
    'MaintenanceTasksBulkImportView',
)

class MaintenanceTasksView(generic.ObjectView):
    queryset = MaintenanceTasks.objects.all()
    

class MaintenanceTasksListView(generic.ObjectListView):
    queryset = MaintenanceTasks.objects.all()
    table = MaintenanceTasksTable
    filterset = MaintenanceTasksFilterSet
    filterset_form = MaintenanceTasksFilterForm
    

class MaintenanceTasksEditView(generic.ObjectEditView):
    queryset = MaintenanceTasks.objects.all()
    form = MaintenanceTasksForm

class MaintenanceTasksDeleteView(generic.ObjectDeleteView):
    queryset = MaintenanceTasks.objects.all() 

class MaintenanceTasksBulkDeleteView(generic.BulkDeleteView):
    queryset = MaintenanceTasks.objects.all()
    table = MaintenanceTasksTable
    
    
class MaintenanceTasksBulkEditView(generic.BulkEditView):
    queryset = MaintenanceTasks.objects.all()
    filterset = MaintenanceTasksFilterSet
    table = MaintenanceTasksTable
    form =  MaintenanceTasksBulkEditForm
    

class MaintenanceTasksBulkImportView(generic.BulkImportView):
    queryset = MaintenanceTasks.objects.all()
    model_form = MaintenanceTasksCSVForm
    table = MaintenanceTasksTable
    