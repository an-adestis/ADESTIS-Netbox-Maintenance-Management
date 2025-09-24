from netbox.views import generic
from adestis_netbox_maintenance_management.forms import *
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.filtersets import *
from adestis_netbox_maintenance_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from utilities.views import ViewTab, register_model_view
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

__all__ = (
    'MaintenanceWindowsView',
    'MaintenanceWindowsListView',
    'MaintenanceWindowsEditView',
    'MaintenanceWindowsDeleteView',
    'MaintenanceWindowsBulkDeleteView',
    'MaintenanceWindowsBulkEditView',
    'MaintenanceWindowsBulkImportView',
    # 'VirtualMachineAffectedMaintenanceWindowsView',
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
    
    
# @register_model_view(VirtualMachine, name='maintenance_windows')
# class VirtualMachineAffectedMaintenanceWindowsView(generic.ObjectChildrenView):
#     queryset = VirtualMachine.objects.all()
#     child_model= MaintenanceWindows
#     table = MaintenanceWindowsTable
#     template_name = "adestis_netbox_maintenance_management/maintenance_windows_virtual_machine.html"
#     actions = {
#         'add': {'add'},
#         'export': {'view'},
#         'bulk_remove_maintenance_window': {'change'},
#     }

#     tab = ViewTab(
#         label=_('Maintenance Windows'),
#         badge=lambda obj: obj.maintenance_window.count(),
#         hide_if_empty=False
#     )

#     def get_children(self, request, parent):
#         return MaintenanceWindows.objects.restrict(request.user, 'view')
    
# @register_model_view(VirtualMachine, 'assign_maintenance_window')
# class VirtualMachineAssignMaintenanceWindows(generic.ObjectEditView):
#     queryset = VirtualMachine.objects.prefetch_related(
#         'maintenance_window', 'tags' 
#     ).all()
    
#     form = VirtualMachineFormAssignMaintenanceWindows
#     template_name = 'adestis_netbox_maintenance_management/assign_maintenance_windows.html'
    
#     def get(self, request, pk):
#         virtual_machine = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(virtual_machine, initial=request.GET)
        
#         return render(request, self.template_name, {
#             'virtual_machine': virtual_machine,
#             'form': form,
#             'return_url': reverse('virtualization:virtualmachine', kwargs={'pk': pk}),
#             'edit_url': reverse('virtualization:virtualmachine_assign_maintenance_window', kwargs={'pk': pk}),
#         })
        
#     def post(self, request, pk):
#         virtual_machine = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(virtual_machine, request.POST)
        
#         if form.is_valid():
            
#             selected_maintenance_windows = form.cleaned_data['maintenance_window']
#             with transaction.atomic():
                
#                 for maintenance_window in MaintenanceWindows.objects.filter(pk__in=selected_maintenance_windows):
#                     virtual_machine.maintenance_window.add(maintenance_window)
                    
#             virtual_machine.save()
            
#             return redirect(virtual_machine.get_absolute_url())
        
#         return render(request, self.template_name,{
#             'virtual_machine': virtual_machine,
#             'form': form,
#             'return_url': virtual_machine.get_absolute_url(),
#             'edit_url': reverse('virtualization:virtualmachine_assign_maintenance_window', kwargs={'pk': pk}),
#         })
        
# @register_model_view(VirtualMachine, 'remove_maintenance_window', path='maintenance_windows/remove')
# class VirtualMachineRemoveViewMaintenanceWindows(generic.ObjectEditView):
#     queryset = VirtualMachine.objects.all()
#     form = VirtualMachineRemoveMaintenanceWindows
#     template_name = 'generic/bulk_remove.html'

#     def post(self, request, pk):

#         virtual_machine = get_object_or_404(self.queryset, pk=pk)

#         if '_confirm' in request.POST:
            
#             form = self.form(request.POST)
#             if form.is_valid():
                
#                 maintenance_windows_pks = form.cleaned_data['pk']
#                 with transaction.atomic():
#                     virtual_machine.maintenance_window.remove(*maintenance_windows_pks)
#                     virtual_machine.save()

#                 messages.success(request, _("Removed {count} maintenance windows from virtual machines{virtual_machine}").format(
#                     count=len(maintenance_windows_pks),
#                     virtual_machine=virtual_machine
#                 ))
#                 return redirect(virtual_machine.get_absolute_url())
#         else:
#             form = self.form(initial={'pk': request.POST.getlist('pk')})

#         selected_objects = MaintenanceWindows.objects.filter(pk__in=form.initial['pk'])
#         maintenance_windows_table = VirtualMachineTableMaintenanceWindows(list(selected_objects), orderable=False)
#         maintenance_windows_table.configure(request)

#         return render(request, self.template_name, {
#             'form': form,
#             'parent_obj': virtual_machine,
#             'table': maintenance_windows_table,
#             'obj_type_plural': 'virtual_machines',
#             'return_url': virtual_machine.get_absolute_url(),
#         })