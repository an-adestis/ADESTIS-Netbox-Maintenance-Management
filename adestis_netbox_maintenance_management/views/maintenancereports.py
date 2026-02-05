from netbox.views import generic
from adestis_netbox_maintenance_management.forms import *
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from adestis_netbox_maintenance_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect

from django.views.generic import TemplateView


__all__ = (
    'MaintenanceReportsView',
    'MaintenanceReportsListView',
    'MaintenanceReportsEditView',
    'MaintenanceReportsDeleteView',
    'MaintenanceReportsBulkEditView',
    'MaintenanceReportsBulkDeleteView',
    
    'MaintenanceReportsBulkImportView'
)

class MaintenanceReportsView(generic.ObjectView):
    queryset = MaintenanceReport.objects.all()
class MaintenanceReportsListView(generic.ObjectListView):
    queryset = MaintenanceReport.objects.all()
    table = MaintenanceReportsTable
    filterset = MaintenanceReportsFilterSet
    filterset_form = MaintenanceReportsFilterForm
    
    
class MaintenanceReportsEditView(generic.ObjectEditView):
    queryset = MaintenanceReport.objects.all()
    form = MaintenanceReportsForm
    
class MaintenanceReportsDeleteView(generic.ObjectDeleteView):
    queryset = MaintenanceReport.objects.all() 

class MaintenanceReportsBulkDeleteView(generic.BulkDeleteView):
    queryset = MaintenanceReport.objects.all()
    table = MaintenanceReportsTable
    
    
class MaintenanceReportsBulkEditView(generic.BulkEditView):
    queryset = MaintenanceReport.objects.all()
    filterset = MaintenanceReportsFilterSet
    table = MaintenanceReportsTable
    form =  MaintenancePlannedActionsBulkEditForm
    

class MaintenanceReportsBulkImportView(generic.BulkImportView):
    queryset = MaintenanceReport.objects.all()
    model_form = MaintenancePlannedActionsCSVForm
    table = MaintenanceReportsTable


