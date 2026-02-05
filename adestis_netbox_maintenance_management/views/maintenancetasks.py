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
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from utilities.views import ViewTab, register_model_view
from django.db.models import Min


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
    
    
@register_model_view(MaintenanceTasks, name='device')
class DeviceAffectedMaintenanceTasksView(generic.ObjectChildrenView):
    queryset = MaintenanceTasks.objects.all()
    child_model= Device
    table = DeviceTable
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_remove_device': {'change'},
    }

    tab = ViewTab(
        label=_('Devices'),
        badge=lambda obj: obj.device.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return Device.objects.restrict(request.user, 'view').filter(tasks_device=parent)
        
@register_model_view(MaintenanceTasks, name='virtual_machine')
class MaintenanceTasksAffectVirtualMachineView(generic.ObjectChildrenView):
    queryset = MaintenanceTasks.objects.all()

    child_model= VirtualMachine
    table = VirtualMachineTableMaintenanceActions

    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_remove_virtual_machine': {'change'},
    }

    tab = ViewTab(
        label=_('Virtual Machine'),
        badge=lambda obj: obj.virtual_machine.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return VirtualMachine.objects.restrict(request.user, 'view').filter(tasks_vm=parent)

