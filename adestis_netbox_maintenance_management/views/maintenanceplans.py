from netbox.views import generic
from adestis_netbox_maintenance_management.forms import *
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from adestis_netbox_maintenance_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from utilities.views import ViewTab, register_model_view

from .maintenancewindows import *
from .maintenanceactions import *
from .maintenanceplannedactions import *
from .maintenancetasks import *
from .maintenanceplans import *
from datetime import datetime, date, timedelta

from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.shortcuts import redirect, render
from adestis_netbox_maintenance_management.models import MaintenancePlans
from io import BytesIO
from django.http import HttpResponse
from fpdf import FPDF, HTMLMixin


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
    template_name = "adestis_netbox_maintenance_management/maintenance_plans.html"
    
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