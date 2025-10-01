from datetime import date
from django.db.models import Q
from extras.jobs import Job

from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlans


class AutoCreateMaintenancePlans(Job):
    class Meta:
        name = "Automatischer Wartungsplan"

    def run(self, data, commit):

        # get date values for today 
        today = date.today()
        weekday = today.weekday()  # Montag = 0

        # Filter windows so only todays windows show up
        active_windows = MaintenanceWindows.objects.filter(
            Q(start_time__isnull=True) | Q(start_time__lte=today),
            Q(end_time__isnull=True) | Q(end_time__gte=today),
            Q(recurrence_type__in=["daily", "weekly", "monthly"])
        )
        # create a new Plan
        created_count = 0
        # to skip already existing Plans
        skipped_count = 0

        window = MaintenanceWindows.objects.all()
        
        for window in active_windows:
        
            is_today = False
            
            # check if schedule_type is daily 
            if window.recurrence_type == "daily":
                is_today = True

            # check if schedule_type is on today weekday
            elif window.recurrence_type == "weekly" and window.weekdays:
                try:
                    weekdays = [int(w.strip()) for w in window.weekdays.split(",")]
                    if weekday in weekdays:
                        is_today = True
                except Exception:
                    continue
            
            # check if schedule_type is on today
            elif window.recurrence_type == "monthly" and window.monthdays:
                try:
                    if window.monthdays == today:
                        is_today = True
                except Exception:
                    continue

            if not is_today:
                continue

            actions = MaintenanceActions.objects.filter(maintenance_window=window)

            if not actions.exists():
                continue
                
            # skip existing Maintenance Plans with a maintenance action
            for action in actions:
                if MaintenancePlans.objects.filter(maintenance_action=action).exists():
                    skipped_count += 1
                    continue

                if not (action.virtual_machine or action.device):
                    continue

                if commit:
                    MaintenancePlans.objects.create(
                        maintenance_action=action
                    )
                created_count += 1
