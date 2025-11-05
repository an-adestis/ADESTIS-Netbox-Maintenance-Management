from netbox.views import generic
from adestis_netbox_maintenance_management.forms import *
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from adestis_netbox_maintenance_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from utilities.views import ViewTab, register_model_view

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
    
    
@register_model_view(MaintenancePlans, name='plans_tasks')
class TasksAffectedMaintenancePlansView(generic.ObjectChildrenView):
    queryset = MaintenancePlans.objects.all()
    child_model= MaintenanceTasks
    table = MaintenanceTasksTable
    # template_name = "adestis_netbox_maintenance_management/maintenance_actions_device.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_remove_maintenance_tasks': {'change'},
    }

    tab = ViewTab(
        label=_('Maintenance Tasks'),
        badge=lambda obj: obj.maintenance_tasks.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return MaintenanceTasks.objects.restrict(request.user, 'view').filter(plans_tasks=parent)