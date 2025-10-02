from datetime import date
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging
# from extras.jobs import Job
from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlans


logger = logging.getLogger(__name__)
@system_job(interval=JobIntervalChoices.INTERVAL_MINUTELY)
class AutoCreateMaintenancePlans(JobRunner):
    class Meta:
        name = "Automatischer Wartungsplan"
        # model = MaintenancePlans

    def run(self, *args, **kwargs):
        # logging.info('job läuft')
        # print("✅ AutoCreateMaintenancePlans wurde ausgeführt (print)")
        
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
        # skip already existing Plans
        skipped_count = 0

        window = MaintenanceWindows.objects.all()
        
        for window in active_windows:
        
            is_today = False
            
            # check if schedule_type is daily 
            if window.recurrence_type == "daily":
                is_today = True
                

            # check if schedule_type is on today's weekday
            elif window.recurrence_type == "weekly" :
                
                if hasattr(window, 'weekdays') and window.weekdays == weekday:
                    is_today = True
            
            # check if schedule_type is on today
            elif window.recurrence_type == "monthly":
                
                if hasattr(window, 'monthdays') and window.monthdays == today.day:
                    is_today = True

            if not is_today:
                continue

            actions = MaintenanceActions.objects.filter(maintenance_window=window).all()

            if not actions.exists():
                continue
                
            # skip existing Maintenance Plans with a maintenance action
            for action in actions:
                if not MaintenancePlans.objects.filter(maintenance_action=action).exists():
                    plan = MaintenancePlans.objects.create(
                        name = action.name,
                        maintenance_action=action
                    )
                    created_count += 1


                # plan = MaintenancePlans.objects.create()
                # plan.maintenance_action.set(actions)
                
                # created_count += 1
