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
    'MaintenancePlannedActionsView',
    'MaintenancePlannedActionsListView',
    'MaintenancePlannedActionsEditView',
    'MaintenancePlannedActionsDeleteView',
    'MaintenancePlannedActionsBulkDeleteView',
    'MaintenancePlannedActionsBulkEditView',
    'MaintenancePlannedActionsBulkImportView',
    'run_myjob',
)

class MaintenancePlannedActionsView(generic.ObjectView):
    queryset = MaintenancePlannedActions.objects.all()
    actions = ()
    template_name = "adestis_netbox_maintenance_management/maintenanceplannedactions.html"

class MaintenancePlannedActionsListView(generic.ObjectListView):
    queryset = MaintenancePlannedActions.objects.all()
    table = MaintenancePlannedActionsTable
    filterset = MaintenancePlannedActionsFilterSet
    filterset_form = MaintenancePlannedActionsFilterForm
    template_name = "adestis_netbox_maintenance_management/maintenanceplannedactions_listview.html"
    def get_extra_context(self, request):
        ctx = super().get_extra_context(request) or {}
        ctx["actions"] = [a for a in ctx.get("actions", []) if a.name not in ["edit", "delete"]]
        return ctx
        
    actions = []
    

class MaintenancePlannedActionsEditView(generic.ObjectEditView):
    queryset = MaintenancePlannedActions.objects.all()
    form = MaintenancePlannedActionsForm

class MaintenancePlannedActionsDeleteView(generic.ObjectDeleteView):
    queryset = MaintenancePlannedActions.objects.all()
    
class MaintenancePlannedActionsBulkDeleteView(generic.BulkDeleteView):
    queryset = MaintenancePlannedActions.objects.all()
    table = MaintenancePlannedActionsTable
    
class MaintenancePlannedActionsBulkEditView(generic.BulkEditView):
    queryset = MaintenancePlannedActions.objects.all()
    filterset = MaintenancePlannedActionsFilterSet
    table = MaintenancePlannedActionsTable
    form =  MaintenancePlannedActionsBulkEditForm
    
class MaintenancePlannedActionsBulkImportView(generic.BulkImportView):
    queryset = MaintenancePlannedActions.objects.all()
    model_form = MaintenancePlannedActionsCSVForm
    table = MaintenancePlannedActionsTable
    
@register_model_view(MaintenancePlannedActions, name='plans_tasks')
class TasksAffectedMaintenancePlannedActionsView(generic.ObjectChildrenView):
    queryset = MaintenancePlannedActions.objects.all()
    child_model= MaintenanceTasks
    table = MaintenanceTasksTable
    template_name = "adestis_netbox_maintenance_management/tasks_affect_plannedactions.html"
    actions = ()

    tab = ViewTab(
        label=_('Maintenance Tasks'),
        badge=lambda obj: obj.maintenance_tasks.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return MaintenanceTasks.objects.restrict(request.user, 'view').filter(plans_tasks=parent)
    
    def get_extra_context(self, request, instance):
        return {
            "actions": None
        }
        
from django.shortcuts import redirect
from adestis_netbox_maintenance_management.plan_jobs import AutoCreateMaintenancePlannedActions
from netbox.jobs import JobRunner
        
def run_myjob(request):
    job_instance = AutoCreateMaintenancePlannedActions(JobRunner)
    job_instance.enqueue()  # Startet den Job im Hintergrund
    return redirect('home')