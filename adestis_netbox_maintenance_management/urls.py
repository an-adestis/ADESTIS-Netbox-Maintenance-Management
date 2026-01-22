from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_maintenance_management.models import *
from adestis_netbox_maintenance_management.views import *
from django.urls import include
from utilities.urls import get_model_urls
from adestis_netbox_maintenance_management import views

urlpatterns = (

    # Maintenance Window
    path('maintenancewindows/', MaintenanceWindowsListView.as_view(),
         name='maintenancewindows_list'),
    path('maintenancewindows/add/', MaintenanceWindowsEditView.as_view(),
         name='maintenancewindows_add'),
    path('maintenancewindows/delete/', MaintenanceWindowsBulkDeleteView.as_view(),
         name='maintenancewindows_bulk_delete'),
    path('maintenancewindows/edit/', MaintenanceWindowsBulkEditView.as_view(),
         name='maintenancewindows_bulk_edit'),
    path('maintenancewindows/import/', MaintenanceWindowsBulkImportView.as_view(),
         name='maintenancewindows_bulk_import'),
    path('maintenancewindows/<int:pk>/',
         MaintenanceWindowsView.as_view(), name='maintenancewindows'),
    path('maintenancewindows/<int:pk>/',
         include(get_model_urls("adestis_netbox_maintenance_management", "maintenancewindows"))),
    path('maintenancewindows/<int:pk>/edit/',
         MaintenanceWindowsEditView.as_view(), name='maintenancewindows_edit'),
    path('maintenancewindows/<int:pk>/delete/',
         MaintenanceWindowsDeleteView.as_view(), name='maintenancewindows_delete'),
    path('maintenancewindows/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='maintenancewindows_changelog', kwargs={
        'model': MaintenanceWindows
    }),
    
     # Maintenance Plans
    path('maintenanceplans/', MaintenancePlansListView.as_view(),
         name='maintenanceplans_list'),
    path('maintenanceplans/add', MaintenancePlansEditView.as_view(),
         name='maintenanceplans_add'),
    path('maintenanceplans/delete/', MaintenancePlansBulkDeleteView.as_view(),
         name='maintenanceplans_bulk_delete'),
    path('maintenanceplans/edit/', MaintenancePlansBulkEditView.as_view(),
         name='maintenanceplans_bulk_edit'),
    path('maintenanceplans/import/', MaintenancePlansBulkImportView.as_view(),
         name='maintenanceplans_bulk_import'),
    path('maintenanceplans/<int:pk>/',
         MaintenancePlansView.as_view(), name='maintenanceplans'),
    path('maintenanceplans/<int:pk>/',
         include(get_model_urls("adestis_netbox_maintenance_management", "maintenanceplans"))),
    path('maintenanceplans/<int:pk>/edit/',
         MaintenancePlansEditView.as_view(), name='maintenanceplans_edit'),
    path('maintenanceplans/<int:pk>/delete/',
         MaintenancePlansDeleteView.as_view(), name='maintenanceplans_delete'),
    
    path(
     'maintenanceplans/pdf/',
     MaintenancePlanPDFView.as_view(),
     name='export_pdf'
     ),

    
    path('maintenanceplans/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='maintenanceplans_changelog', kwargs={
        'model': MaintenancePlans
    }),
    
    # Maintenance Actions
    path('maintenanceactions/', MaintenanceActionsListView.as_view(),
         name='maintenanceactions_list'),
    path('maintenanceactions/add/', MaintenanceActionsEditView.as_view(),
         name='maintenanceactions_add'),
    path('maintenanceactions/delete/', MaintenanceActionsBulkDeleteView.as_view(),
         name='maintenanceactions_bulk_delete'),
    path('maintenanceactions/edit/', MaintenanceActionsBulkEditView.as_view(),
         name='maintenanceactions_bulk_edit'),
    path('maintenanceactions/import/', MaintenanceActionsBulkImportView.as_view(),
         name='maintenanceactions_bulk_import'),
    path('maintenanceactions/<int:pk>/',
         MaintenanceActionsView.as_view(), name='maintenanceactions'),
    path('maintenanceactions/<int:pk>/',
         include(get_model_urls("adestis_netbox_maintenance_management", "maintenanceactions"))),
    path('maintenanceactions/<int:pk>/edit/',
         MaintenanceActionsEditView.as_view(), name='maintenanceactions_edit'),
    path('maintenanceactions/<int:pk>/delete/',
         MaintenanceActionsDeleteView.as_view(), name='maintenanceactions_delete'),
    path('maintenanceactions/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='maintenanceactions_changelog', kwargs={
        'model': MaintenanceActions}),  
    path('maintenanceactions/devices/', DeviceAffectedMaintenanceActionsView.as_view(),
         name='maintenanceactionsdevices_list'),
    path('maintenanceactions/virtualmachines/', VirtualMachineAffectedMaintenanceActionsView.as_view(),
         name='maintenanceactionsvirtualmachines_list'),
    
    # Maintenance Tasks
    path('maintenancetasks/', MaintenanceTasksListView.as_view(),
         name='maintenancetasks_list'),
    path('maintenancetasks/add/', MaintenanceTasksEditView.as_view(),
         name='maintenancetasks_add'),
    path('maintenancetasks/delete/', MaintenanceTasksBulkDeleteView.as_view(),
         name='maintenancetasks_bulk_delete'),
    path('maintenancetasks/edit/', MaintenanceTasksBulkEditView.as_view(),
         name='maintenancetasks_bulk_edit'),
    path('maintenancetasks/import/', MaintenanceTasksBulkImportView.as_view(),
         name='maintenancetasks_bulk_import'),
    path('maintenancetasks/<int:pk>/',
         MaintenanceTasksView.as_view(), name='maintenancetasks'),
    path('maintenancetasks/<int:pk>/',
         include(get_model_urls("adestis_netbox_maintenance_management", "maintenancetasks"))),
    path('maintenancetasks/<int:pk>/edit/',
         MaintenanceTasksEditView.as_view(), name='maintenancetasks_edit'),
    path('maintenancetasks/<int:pk>/delete/',
         MaintenanceTasksDeleteView.as_view(), name='maintenancetasks_delete'),
    path('maintenancetasks/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='maintenancetasks_changelog', kwargs={
        'model': MaintenanceTasks
    }),
    
    # Maintenance Planned Actions
    path('maintenanceplannedactions/', MaintenancePlannedActionsListView.as_view(),
         name='maintenanceplannedactions_list'),
    path('maintenanceplannedactions/', MaintenancePlannedActionsEditView.as_view(),
         name='maintenanceplannedactions_add'),
    path('maintenanceplannedactions/delete/', MaintenancePlannedActionsBulkDeleteView.as_view(),
         name='maintenanceplannedactions_bulk_delete'),
    path('maintenanceplannedactions/edit/', MaintenancePlannedActionsBulkEditView.as_view(),
         name='maintenanceplannedactions_bulk_edit'),
    path('maintenanceplannedactions/import/', MaintenancePlannedActionsBulkImportView.as_view(),
         name='maintenanceplannedactions_bulk_import'),
    path('maintenanceplannedactions/<int:pk>/',
         MaintenancePlannedActionsView.as_view(), name='maintenanceplannedactions'),
    path('maintenanceplannedactions/<int:pk>/',
         include(get_model_urls("adestis_netbox_maintenance_management", "maintenanceplannedactions"))),
    path('maintenanceplannedactions/<int:pk>/edit/',
         MaintenancePlannedActionsEditView.as_view(), name='maintenanceplannedactions_edit'),
    path('maintenanceplannedactions/<int:pk>/delete/',
         MaintenancePlannedActionsDeleteView.as_view(), name='maintenanceplannedactions_delete'),
    path('maintenanceplannedactions/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='maintenanceplannedactions_changelog', kwargs={
        'model': MaintenancePlannedActions
    }),
    
    path(
          'maintenanceplannedactions/pdf/<int:pk>/',
          MaintenanceActionPlanPDFView.as_view(),
          name='export_planned_action_pdf'
     ),

    # Maintenance Reports
    path('maintenancereports/', MaintenanceReportsListView.as_view(),
         name='maintenancereport_list'),
    path('maintenancereports/add/', MaintenanceReportsEditView.as_view(),
         name='maintenancereport_add'),
    path('maintenancereports/<int:pk>/edit/',
         MaintenanceReportsEditView.as_view(), name='maintenancereport_edit'),
    path('maintenancereports/delete/', MaintenanceReportsBulkDeleteView.as_view(),
         name='maintenancereport_bulk_delete'),
    path('maintenancereports/edit/', MaintenanceReportsBulkEditView.as_view(),
         name='maintenancereport_bulk_edit'),
    path('maintenancereports/import/', MaintenanceReportsBulkImportView.as_view(),
         name='maintenancereport_bulk_import'),
    path('maintenancereports/<int:pk>/',
         MaintenanceReportsView.as_view(), name='maintenancereports'),
    path('maintenancereports/<int:pk>/delete/',
         MaintenanceReportsDeleteView.as_view(), name='maintenancereport_delete'),
    path('maintenancereports/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='maintenancereport_changelog', kwargs={
        'model': MaintenanceReport}), 
)