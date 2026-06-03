from netbox.search import SearchIndex, register_search
from adestis_netbox_maintenance_management.models import *


@register_search
class MaintenanceActionsIndex(SearchIndex):
    model = MaintenanceActions
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 2000),
    )


@register_search
class MaintenanceWindowsIndex(SearchIndex):
    model = MaintenanceWindows
    fields = (
        ('name', 100),
        ('schedule_type', 1000),
        ('description', 500),
        ('week_in_month', 1000),
        ('start_day', 1000),
        ('end_day', 1000),
        ('recurrence_type', 1000),
        ('weekdays', 1000),
        ('monthdays', 1000),
        ('day_of_month', 1000),
        ('special_ordinal', 1000),
        ('start_time', 1000),
        ('end_time', 1000),
        
    )


@register_search
class MaintenancePlannedActionsIndex(SearchIndex):
    model = MaintenancePlannedActions
    fields = (
        ('name', 100),
        ('grouping_key', 500),
        ('description', 1000),
    )


@register_search
class MaintenanceTasksIndex(SearchIndex):
    model = MaintenanceTasks
    fields = (
        ('name', 100),
        ('status', 1000),
        ('next_due_date', 1000),
        ('comments', 1000),
        ('description', 1000),
    )
    
@register_search
class MaintenancePlansIndex(SearchIndex):
    model = MaintenancePlans
    fields = (
        ('name', 100),
        ('reference_number', 1000),
        ('version', 1000),
        ('description', 1000),
    )