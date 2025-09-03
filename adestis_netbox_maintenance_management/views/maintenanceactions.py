from netbox.views import generic
from adestis_netbox_maintenance_management.forms.maintenanceactions import *
from adestis_netbox_maintenance_management.models.maintenanceactions import *
from adestis_netbox_maintenance_management.filtersets.maintenanceactions import *
from adestis_netbox_maintenance_management.tables.maintenanceactions import *
from netbox.views import generic
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from utilities.views import ViewTab, register_model_view
from dcim.models import *
from dcim.forms import *
from dcim.tables import *
from dcim.filtersets import *
from netbox.constants import DEFAULT_ACTION_PERMISSIONS
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
from django.db import transaction
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

__all__ = (
    'MaintenanceActionsView',
    'MaintenanceActionsListView',
    'MaintenanceActionsEditView',
    'MaintenanceActionsDeleteView',
    'MaintenanceActionsBulkDeleteView',
    'MaintenanceActionsBulkEditView',
    'MaintenanceActionsBulkImportView',
    
    'DeviceAffectedMaintenanceActionsView',
    'DeviceAffectedMaintenanceActionsView',
    'MaintenanceActionsAssignDevice',
    'MaintenanceActionsRemoveDeviceView',
    
    'VirtualMachineAffectedMaintenanceActionsView',
    'VirtualMachineAffectedMaintenanceActionsView',
    'MaintenanceActionsAssignDevice',
    'MaintenanceActionsRemoveVirtualMachineView',
)

class MaintenanceActionsView(generic.ObjectView):
    queryset = MaintenanceActions.objects.all()
    

class MaintenanceActionsListView(generic.ObjectListView):
    queryset = MaintenanceActions.objects.all()
    table = MaintenanceActionsTable
    filterset = MaintenanceActionsFilterSet
    filterset_form = MaintenanceActionsFilterForm
    

class MaintenanceActionsEditView(generic.ObjectEditView):
    queryset = MaintenanceActions.objects.all()
    form = MaintenanceActionsForm
    # template_name = "adestis_netbox_maintenance_management/maintenanceactionsadd.html"


class MaintenanceActionsDeleteView(generic.ObjectDeleteView):
    queryset = MaintenanceActions.objects.all() 

class MaintenanceActionsBulkDeleteView(generic.BulkDeleteView):
    queryset = MaintenanceActions.objects.all()
    table = MaintenanceActionsTable
    
    
class MaintenanceActionsBulkEditView(generic.BulkEditView):
    queryset = MaintenanceActions.objects.all()
    filterset = MaintenanceActionsFilterSet
    table = MaintenanceActionsTable
    form =  MaintenanceActionsBulkEditForm
    

class MaintenanceActionsBulkImportView(generic.BulkImportView):
    queryset = MaintenanceActions.objects.all()
    model_form = MaintenanceActionsCSVForm
    table = MaintenanceActionsTable
    
@register_model_view(MaintenanceActions, name='device')
class DeviceAffectedMaintenanceActionsView(generic.ObjectChildrenView):
    queryset = MaintenanceActions.objects.all()
    child_model= Device
    table = DeviceTableMaintenanceActions
    template_name = "adestis_netbox_maintenance_management/device.html"
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
        return Device.objects.restrict(request.user, 'view').filter(maintenance_actions=parent)

@register_model_view(Device, name='maintenance_actions')
class DeviceAffectedMaintenanceActionsView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    child_model= MaintenanceActions
    table = MaintenanceActionsTableTab
    template_name = "adestis_netbox_maintenance_management/maintenance_actions_device.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_maintenance_actions': {'change'},
    }

    tab = ViewTab(
        label=_('Maintenance Actions'),
        badge=lambda obj: obj.maintenance_actions.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return MaintenanceActions.objects.restrict(request.user, 'view').filter(device=parent)
      
@register_model_view(MaintenanceActions, 'assign_device')
class MaintenanceActionsAssignDevice(generic.ObjectEditView):
    queryset = MaintenanceActions.objects.prefetch_related(
        'device', 'tags', 
    ).all()
    
    form = MaintenanceActionsAssignDeviceForm
    template_name = 'adestis_netbox_maintenance_management/assign_device.html'

    def get(self, request, pk):
        maintenance_actions = get_object_or_404(self.queryset, pk=pk)
        form = self.form(maintenance_actions,  initial=request.GET)

        return render(request, self.template_name, {
            'maintenance_actions': maintenance_actions,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions_assign_device', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        maintenance_actions = get_object_or_404(self.queryset, pk=pk)
        form = self.form(maintenance_actions, request.POST)

        if form.is_valid():
            
            selected_devices = form.cleaned_data['device']
            with transaction.atomic():
                
                for device in Device.objects.filter(pk__in=selected_devices): 
                    maintenance_actions.device.add(device)
            
            maintenance_actions.save()
            
            return redirect(maintenance_actions.get_absolute_url())

        return render(request, self.template_name, {
            'maintenance_actions': maintenance_actions,
            'form': form,
            'return_url': maintenance_actions.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenance_actions_assign_device', kwargs={'pk': pk}),
        })
        
@register_model_view(MaintenanceActions, 'remove_device', path='device/remove')
class MaintenanceActionsRemoveDeviceView(generic.ObjectEditView):
    queryset = MaintenanceActions.objects.all()
    form = MaintenanceActionsRemoveDevice
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        maintenance_actions = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                device_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    maintenance_actions.device.remove(*device_pks)
                    maintenance_actions.save()

                messages.success(request, _("Removed {count} devices from maintenance actions{maintenance_actions}").format(
                    count=len(device_pks),
                    maintenance_actions=maintenance_actions
                ))
                return redirect(maintenance_actions.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = Device.objects.filter(pk__in=form.initial['pk'])
        device_table = DeviceTable(list(selected_objects), orderable=False)
        device_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': maintenance_actions,
            'table': device_table,
            'obj_type_plural': 'devices',
            'return_url': maintenance_actions.get_absolute_url(),
        })
        
@register_model_view(MaintenanceActions, name='virtual_machine')
class VirtualMachineAffectedMaintenanceActionsView(generic.ObjectChildrenView):
    queryset = MaintenanceActions.objects.all()
    child_model= VirtualMachine
    table = VirtualMachineTableMaintenanceActions
    template_name = "adestis_netbox_maintenance_management/virtual_machine.html"
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
        return VirtualMachine.objects.restrict(request.user, 'view').filter(maintenance_actions=parent)

@register_model_view(VirtualMachine, name='maintenance_actions')
class VirtualMachineAffectedMaintenanceActionsView(generic.ObjectChildrenView):
    queryset = VirtualMachine.objects.all()
    child_model= MaintenanceActions
    table = MaintenanceActionsTableTab
    template_name = "adestis_netbox_maintenance_management/maintenance_actions_virtual_machine.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        # 'bulk_import': {'add'},
        # 'bulk_edit': {'change'},
        'bulk_remove_maintenance_actions': {'change'},
    }

    tab = ViewTab(
        label=_('Maintenance Actions'),
        badge=lambda obj: obj.maintenance_actions.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return MaintenanceActions.objects.restrict(request.user, 'view').filter(virtual_machine=parent)
      
@register_model_view(MaintenanceActions, 'assign_virtual_machine')
class MaintenanceActionsAssignDevice(generic.ObjectEditView):
    queryset = MaintenanceActions.objects.prefetch_related(
        'virtual_machine', 'tags', 
    ).all()
    
    form = MaintenanceActionsAssignVirtualMachineForm
    template_name = 'adestis_netbox_maintenance_management/assign_virtual_machine.html'

    def get(self, request, pk):
        maintenance_actions = get_object_or_404(self.queryset, pk=pk)
        form = self.form(maintenance_actions,  initial=request.GET)

        return render(request, self.template_name, {
            'maintenance_actions': maintenance_actions,
            'form': form,
            'return_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions_assign_virtual_machine', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        maintenance_actions = get_object_or_404(self.queryset, pk=pk)
        form = self.form(maintenance_actions, request.POST)

        if form.is_valid():
            
            selected_virtual_machines = form.cleaned_data['virtual_machine']
            with transaction.atomic():
                
                for virtual_machine in VirtualMachine.objects.filter(pk__in=selected_virtual_machines): 
                    maintenance_actions.virtual_machine.add(virtual_machine)
            
            maintenance_actions.save()
            
            return redirect(maintenance_actions.get_absolute_url())

        return render(request, self.template_name, {
            'maintenance_actions': maintenance_actions,
            'form': form,
            'return_url': maintenance_actions.get_absolute_url(),
            'edit_url': reverse('plugins:adestis_netbox_maintenance_management:maintenance_actions_assign_virtual_machine', kwargs={'pk': pk}),
        })
        
@register_model_view(MaintenanceActions, 'remove_virtual_machine', path='virtual_machine/remove')
class MaintenanceActionsRemoveVirtualMachineView(generic.ObjectEditView):
    queryset = MaintenanceActions.objects.all()
    form = MaintenanceActionsRemoveVirtualMachine
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        maintenance_actions = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                virtual_machine_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    maintenance_actions.virtual_machine.remove(*virtual_machine_pks)
                    maintenance_actions.save()

                messages.success(request, _("Removed {count} virtual_machines from maintenance actions{maintenance_actions}").format(
                    count=len(virtual_machine_pks),
                    maintenance_actions=maintenance_actions
                ))
                return redirect(maintenance_actions.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = VirtualMachine.objects.filter(pk__in=form.initial['pk'])
        virtual_machine_table = VirtualMachineTable(list(selected_objects), orderable=False)
        virtual_machine_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': maintenance_actions,
            'table': virtual_machine_table,
            'obj_type_plural': 'virtual_machines',
            'return_url': maintenance_actions.get_absolute_url(),
        })
    