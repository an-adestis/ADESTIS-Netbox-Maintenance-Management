from netbox.views import generic
from adestis_netbox_maintenance_management.forms import *
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from adestis_netbox_maintenance_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect

__all__ = (
    'MaintenancePlansView',
    'MaintenancePlansListView',
    'MaintenancePlansEditView',
    'MaintenancePlansDeleteView',
    'MaintenancePlansBulkDeleteView',
    'MaintenancePlansBulkEditView',
    'MaintenancePlansBulkImportView',
)

class MaintenancePlansView(generic.ObjectView):
    queryset = MaintenancePlans.objects.all()
    

class MaintenancePlansListView(generic.ObjectListView):
    queryset = MaintenancePlans.objects.all()
    table = MaintenancePlansTable
    filterset = MaintenancePlansFilterSet
    filterset_form = MaintenancePlansFilterForm
    

class MaintenancePlansEditView(generic.ObjectEditView):
    queryset = MaintenancePlans.objects.all()
    form = MaintenancePlansForm

class MaintenancePlansDeleteView(generic.ObjectDeleteView):
    queryset = MaintenancePlans.objects.all() 

class MaintenancePlansBulkDeleteView(generic.BulkDeleteView):
    queryset = MaintenancePlans.objects.all()
    table = MaintenancePlansTable
    
    
class MaintenancePlansBulkEditView(generic.BulkEditView):
    queryset = MaintenancePlans.objects.all()
    filterset = MaintenancePlansFilterSet
    table = MaintenancePlansTable
    form =  MaintenancePlansBulkEditForm
    

class MaintenancePlansBulkImportView(generic.BulkImportView):
    queryset = MaintenancePlans.objects.all()
    model_form = MaintenancePlansCSVForm
    table = MaintenancePlansTable
    