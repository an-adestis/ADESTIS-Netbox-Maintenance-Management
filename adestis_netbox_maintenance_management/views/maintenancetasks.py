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
    
    
# @register_model_view(MaintenanceActions, name='device')
# class DeviceAffectedMaintenanceActionsView(generic.ObjectChildrenView):
#     queryset = MaintenanceActions.objects.all()
#     child_model= Device
#     table = DeviceTable
#     template_name = "adestis_netbox_maintenance_management/device.html"
#     actions = {
#         'add': {'add'},
#         'export': {'view'},
#         'bulk_remove_device': {'change'},
#     }

#     tab = ViewTab(
#         label=_('Devices'),
#         badge=lambda obj: obj.device.count(),
#         weight=600
#     )

#     def get_children(self, request, parent):
#         return Device.objects.restrict(request.user, 'view').filter(maintenance_actions=parent)

# @register_model_view(Device, name='maintenance_actions')
# class DeviceAffectedMaintenanceActionsView(generic.ObjectChildrenView):
#     queryset = Device.objects.all()
#     child_model= MaintenanceActions
#     table = MaintenanceActionsTableTab
#     template_name = "adestis_netbox_maintenance_management/maintenance_actions_device.html"
#     actions = {
#         'add': {'add'},
#         'export': {'view'},
#         # 'bulk_import': {'add'},
#         # 'bulk_edit': {'change'},
#         'bulk_remove_maintenance_actions': {'change'},
#     }

#     tab = ViewTab(
#         label=_('Maintenance Actions'),
#         badge=lambda obj: obj.maintenance_actions.count(),
#         hide_if_empty=False
#     )

#     def get_children(self, request, parent):
#         return MaintenanceActions.objects.restrict(request.user, 'view').filter(device=parent)
      
# @register_model_view(MaintenanceActions, 'assign_device')
# class MaintenanceActionsAssignDevice(generic.ObjectEditView):
#     queryset = MaintenanceActions.objects.prefetch_related(
#         'device', 'tags', 
#     ).all()
    
#     form = MaintenanceActionsAssignDeviceForm
#     template_name = 'adestis_netbox_maintenance_management/assign_device.html'

#     def get(self, request, pk):
#         maintenance_actions = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(maintenance_actions,  initial=request.GET)

#         return render(request, self.template_name, {
#             'maintenance_actions': maintenance_actions,
#             'form': form,
#             'return_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions', kwargs={'pk': pk}),
#             'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions_assign_device', kwargs={'pk': pk}),
#         })

#     def post(self, request, pk):
#         maintenance_actions = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(maintenance_actions, request.POST)

#         if form.is_valid():
            
#             selected_devices = form.cleaned_data['device']
#             with transaction.atomic():
                
#                 for device in Device.objects.filter(pk__in=selected_devices): 
#                     maintenance_actions.device.add(device)
            
#             maintenance_actions.save()
            
#             return redirect(maintenance_actions.get_absolute_url())

#         return render(request, self.template_name, {
#             'maintenance_actions': maintenance_actions,
#             'form': form,
#             'return_url': maintenance_actions.get_absolute_url(),
#             'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenance_actions_assign_device', kwargs={'pk': pk}),
#         })



# @register_model_view(Device, 'assign_maintenance_actions') 
# class DeviceAssignMaintenanceActions(generic.ObjectEditView):
#     queryset = Device.objects.prefetch_related(
#         'maintenance_actions', 'tags'
#     ).all()
    
#     form = DeviceFormAssignMaintenanceAction
#     template_name = 'adestis_netbox_maintenance_management/assign_maintenance_actions.html'
    
#     def get(self, request, pk):
#         device = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(data=request.GET, device = device)
        
#         return render (request, self.template_name, {
#             'device': device,
#             'form': form,
#             'return_url': reverse('dcim:device', kwargs={'pk': pk}),
#             'edit_url': reverse('dcim:device_assign_maintenance_actions', kwargs={'pk':pk}),
#         })
    
#     def post(self, request, pk):
#         device = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(data=request.POST, device=device)

#         if form.is_valid():
            
#             selected_maintenance_actions = form.cleaned_data['maintenance_actions']
#             with transaction.atomic():
                
#                 for maintenance_actions in MaintenanceActions.objects.filter(pk__in=selected_maintenance_actions):
#                     device.maintenance_actions.add(maintenance_actions)
                    
#             device.save()
            
#             return redirect(device.get_absolute_url())
        
#         return render(request, self.template_name,{
#             'device': device,
#             'form': form,
#             'return_url': device.get_absolute_url(),
#             'edit_url': reverse('dcim:device_assign_maintenance_actions', kwargs={'pk': pk}),
#         })
            
            
# @register_model_view(MaintenanceActions, 'remove_device', path='device/remove')
# class MaintenanceActionsRemoveDeviceView(generic.ObjectEditView):
#     queryset = MaintenanceActions.objects.all()
#     form = MaintenanceActionsRemoveDevice
#     template_name = 'generic/bulk_remove.html'

#     def post(self, request, pk):

#         maintenance_actions = get_object_or_404(self.queryset, pk=pk)

#         if '_confirm' in request.POST:
            
#             form = self.form(request.POST)
#             if form.is_valid():
                
#                 device_pks = form.cleaned_data['pk']
#                 with transaction.atomic():
#                     maintenance_actions.device.remove(*device_pks)
#                     maintenance_actions.save()

#                 messages.success(request, _("Removed {count} devices from maintenance actions{maintenance_actions}").format(
#                     count=len(device_pks),
#                     maintenance_actions=maintenance_actions
#                 ))
#                 return redirect(maintenance_actions.get_absolute_url())
#         else:
#             form = self.form(initial={'pk': request.POST.getlist('pk')})

#         selected_objects = Device.objects.filter(pk__in=form.initial['pk'])
#         device_table = DeviceTable(list(selected_objects), orderable=False)
#         device_table.configure(request)

#         return render(request, self.template_name, {
#             'form': form,
#             'parent_obj': maintenance_actions,
#             'table': device_table,
#             'obj_type_plural': 'devices',
#             'return_url': maintenance_actions.get_absolute_url(),
#         })
        
# @register_model_view(Device, 'remove_maintenance_actions', path='maintenance_actions/remove')
# class DeviceRemoveViewMaintenanceActions(generic.ObjectEditView):
#     queryset = Device.objects.all()
#     form = DeviceRemoveMaintenanceActions
#     template_name = 'generic/bulk_remove.html'

#     def post(self, request, pk):

#         device = get_object_or_404(self.queryset, pk=pk)

#         if '_confirm' in request.POST:
            
#             form = self.form(request.POST)
#             if form.is_valid():
                
#                 maintenance_actions_pks = form.cleaned_data['pk']
#                 with transaction.atomic():
#                     device.maintenance_actions.remove(*maintenance_actions_pks)
#                     device.save()

#                 messages.success(request, _("Removed {count} maintenance windows from device {device}").format(
#                     count=len(maintenance_actions_pks),
#                     device=device
#                 ))
#                 return redirect(device.get_absolute_url())
#         else:
#             form = self.form(initial={'pk': request.POST.getlist('pk')})

#         selected_objects = MaintenanceActions.objects.filter(pk__in=form.initial['pk'])
#         maintenance_actions_table = DeviceTableMaintenanceActions(list(selected_objects), orderable=False)
#         maintenance_actions_table.configure(request)

#         return render(request, self.template_name, {
#             'form': form,
#             'parent_obj': device,
#             'table': maintenance_actions_table,
#             'obj_type_plural': 'devices',
#             'return_url': device.get_absolute_url(),
#         })
        
# @register_model_view(MaintenanceActions, name='virtual_machine')
# class MaintenanceActionsAffectVirtualMachineView(generic.ObjectChildrenView):
#     queryset = MaintenanceActions.objects.all()
#     child_model= VirtualMachine
#     table = VirtualMachineTableMaintenanceActions
#     template_name = "adestis_netbox_maintenance_management/virtual_machine.html"
#     actions = {
#         'add': {'add'},
#         'export': {'view'},
#         'bulk_remove_virtual_machine': {'change'},
#     }

#     tab = ViewTab(
#         label=_('Virtual Machine'),
#         badge=lambda obj: obj.virtual_machine.count(),
#         weight=600
#     )

#     def get_children(self, request, parent):
#         return VirtualMachine.objects.restrict(request.user, 'view').filter(maintenance_actions=parent)

# @register_model_view(VirtualMachine, name='maintenance_actions')
# class VirtualMachineAffectedMaintenanceActionsView(generic.ObjectChildrenView):
#     queryset = VirtualMachine.objects.all()
#     child_model= MaintenanceActions
#     table = MaintenanceActionsTableTab
#     template_name = "adestis_netbox_maintenance_management/maintenance_actions_virtual_machine.html"
#     actions = {
#         'add': {'add'},
#         'export': {'view'},
#         # 'bulk_import': {'add'},
#         # 'bulk_edit': {'change'},
#         'bulk_remove_maintenance_actions': {'change'},
#     }

#     tab = ViewTab(
#         label=_('Maintenance Actions'),
#         badge=lambda obj: obj.maintenance_actions.count(),
#         hide_if_empty=False
#     )

#     def get_children(self, request, parent):
#         return MaintenanceActions.objects.restrict(request.user, 'view').filter(virtual_machine=parent)
      
# @register_model_view(MaintenanceActions, 'assign_virtual_machine')
# class MaintenanceActionsAssignVirtualMachine(generic.ObjectEditView):
#     queryset = MaintenanceActions.objects.prefetch_related(
#         'virtual_machine', 'tags', 
#     ).all()
    
#     form = MaintenanceActionsAssignVirtualMachineForm
#     template_name = 'adestis_netbox_maintenance_management/assign_virtual_machine.html'

#     def get(self, request, pk):
#         maintenance_actions = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(maintenance_actions,  initial=request.GET)

#         return render(request, self.template_name, {
#             'maintenance_actions': maintenance_actions,
#             'form': form,
#             'return_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions', kwargs={'pk': pk}),
#             'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions_assign_virtual_machine', kwargs={'pk': pk}),
#         })

#     def post(self, request, pk):
#         maintenance_actions = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(maintenance_actions, request.POST)

#         if form.is_valid():
            
#             selected_virtual_machines = form.cleaned_data['virtual_machine']
#             with transaction.atomic():
                
#                 for virtual_machine in VirtualMachine.objects.filter(pk__in=selected_virtual_machines): 
#                     maintenance_actions.virtual_machine.add(virtual_machine)
            
#             maintenance_actions.save()
            
#             return redirect(maintenance_actions.get_absolute_url())

#         return render(request, self.template_name, {
#             'maintenance_actions': maintenance_actions,
#             'form': form,
#             'return_url': maintenance_actions.get_absolute_url(),
#             'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenance_actions_assign_virtual_machine', kwargs={'pk': pk}),
#         })
        
# @register_model_view(MaintenanceActions, 'remove_virtual_machine', path='virtual_machine/remove')
# class MaintenanceActionsRemoveVirtualMachineView(generic.ObjectEditView):
#     queryset = MaintenanceActions.objects.all()
#     form = MaintenanceActionsRemoveVirtualMachine
#     template_name = 'generic/bulk_remove.html'

#     def post(self, request, pk):

#         maintenance_actions = get_object_or_404(self.queryset, pk=pk)

#         if '_confirm' in request.POST:
            
#             form = self.form(request.POST)
#             if form.is_valid():
                
#                 virtual_machine_pks = form.cleaned_data['pk']
#                 with transaction.atomic():
#                     maintenance_actions.virtual_machine.remove(*virtual_machine_pks)
#                     maintenance_actions.save()

#                 messages.success(request, _("Removed {count} virtual_machines from maintenance actions{maintenance_actions}").format(
#                     count=len(virtual_machine_pks),
#                     maintenance_actions=maintenance_actions
#                 ))
#                 return redirect(maintenance_actions.get_absolute_url())
#         else:
#             form = self.form(initial={'pk': request.POST.getlist('pk')})

#         selected_objects = VirtualMachine.objects.filter(pk__in=form.initial['pk'])
#         virtual_machine_table = VirtualMachineTable(list(selected_objects), orderable=False)
#         virtual_machine_table.configure(request)

#         return render(request, self.template_name, {
#             'form': form,
#             'parent_obj': maintenance_actions,
#             'table': virtual_machine_table,
#             'obj_type_plural': 'virtual_machines',
#             'return_url': maintenance_actions.get_absolute_url(),
#         })
        
# @register_model_view(VirtualMachine, 'assign_maintenance_actions') 
# class VirtualMachineAssignMaintenanceActions(generic.ObjectEditView):
#     queryset = VirtualMachine.objects.prefetch_related(
#         'maintenance_actions', 'tags'
#     ).all()
    
#     form = VirtualMachineFormAssignMaintenanceAction
#     template_name = 'adestis_netbox_maintenance_management/vm_assign_maintenance_actions.html'
    
#     def get(self, request, pk):
#         virtual_machine = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(data=request.GET, virtual_machine = virtual_machine)
        
        
#         return render (request, self.template_name, {
#             'virtual_machine': virtual_machine,
#             'form': form,
#             'return_url': reverse('virtualization:virtualmachine', kwargs={'pk': pk}),
#             'edit_url': reverse('virtualization:virtualmachine_assign_maintenance_actions', kwargs={'pk':pk}),
#         })
    
#     def post(self, request, pk):
#         virtual_machine = get_object_or_404(self.queryset, pk=pk)
#         form = self.form(data=request.POST, virtual_machine=virtual_machine)

#         if form.is_valid():
            
#             selected_maintenance_actions = form.cleaned_data['maintenance_actions']
#             with transaction.atomic():
                
#                 for maintenance_actions in MaintenanceActions.objects.filter(pk__in=selected_maintenance_actions):
#                     virtual_machine.maintenance_actions.add(maintenance_actions)
                    
#             virtual_machine.save()
            
#             return redirect(virtual_machine.get_absolute_url())
        
#         return render(request, self.template_name,{
#             'virtual_machine': virtual_machine,
#             'form': form,
#             'return_url': virtual_machine.get_absolute_url(),
#             'edit_url': reverse('virtualization:virtualmachine_assign_maintenance_actions', kwargs={'pk': pk}),
#         })
        
# @register_model_view(VirtualMachine, 'remove_maintenance_actions', path='maintenance_actions/remove')
# class VirtualMachineRemoveViewMaintenanceActions(generic.ObjectEditView):
#     queryset = VirtualMachine.objects.all()
#     form = VirtualMachineRemoveMaintenanceActions
#     template_name = 'generic/bulk_remove.html'

#     def post(self, request, pk):

#         virtual_machine = get_object_or_404(self.queryset, pk=pk)

#         if '_confirm' in request.POST:
            
#             form = self.form(request.POST)
#             if form.is_valid():
                
#                 maintenance_actions_pks = form.cleaned_data['pk']
#                 with transaction.atomic():
#                     virtual_machine.maintenance_actions.remove(*maintenance_actions_pks)
#                     virtual_machine.save()

#                 messages.success(request, _("Removed {count} maintenance windows from virtual machines{virtual_machine}").format(
#                     count=len(maintenance_actions_pks),
#                     virtual_machine=virtual_machine
#                 ))
#                 return redirect(virtual_machine.get_absolute_url())
#         else:
#             form = self.form(initial={'pk': request.POST.getlist('pk')})

#         selected_objects = MaintenanceActions.objects.filter(pk__in=form.initial['pk'])
#         maintenance_actions_table = VirtualMachineTableMaintenanceActions(list(selected_objects), orderable=False)
#         maintenance_actions_table.configure(request)

#         return render(request, self.template_name, {
#             'form': form,
#             'parent_obj': virtual_machine,
#             'table': maintenance_actions_table,
#             'obj_type_plural': 'virtual_machines',
#             'return_url': virtual_machine.get_absolute_url(),
#         })