from datetime import date
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging
# from extras.jobs import Job
from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlans, MaintenanceTasks


logger = logging.getLogger(__name__)

class AutoCreateMaintenanceTasks(JobRunner):
    class Meta:
        name = "Automatischer Wartungsplan"
        # model = MaintenancePlans

    def run(self, *args, **kwargs):
        
        # get date values for today 
        today = date.today()
        # weekday = today.weekday()  # Montag = 0

        # Filter windows so only todays windows show up 
        # active_windows = MaintenanceWindows.objects.filter(
        #     Q(start_day__isnull=True) | Q(start_day__lte=today),
        #     Q(end_time__isnull=True) | Q(end_time__gte=today),
        #     Q(recurrence_type__in=["daily", "weekly", "monthly"])
        # )
        # create a new Plan
        created_count = 0
        # skip already existing Plans
        skipped_count = 0

        window = MaintenanceWindows.objects.all()
        
        # for window in active_windows:
        
        #     is_today = False
            
        #     # check if schedule_type is daily 
        #     if window.recurrence_type == "daily":
        #         is_today = True
                

        #     # check if schedule_type is on today's weekday
        #     elif window.recurrence_type == "weekly":
        #         try:
        #             if window.weekdays and int(window.weekdays) == weekday:
        #                 is_today = True
        #         except ValueError:
        #             # logger.warning(f"Ungültiger Wert in 'weekdays': {window.weekdays}")
        #             continue

        #     elif window.recurrence_type == "monthly":
        #         if window.monthdays and window.monthdays.day == today.day:
        #             is_today = True

        #     if not is_today:
        #         continue

        actions = MaintenanceActions.objects.filter(maintenance_window=window).all()


        for action in actions:
                if not MaintenanceTasks.objects.filter(maintenance_action=action).exists():
                    task = MaintenanceTasks.objects.create(
                        name = action.name + " " + str(today),
                        maintenance_action=action, 
                        maintenance_windows = window,
                        comments = action.comments,
                    )
                    # task.maintenance_action.set([action])
                    # task.maintenance_windows.set([window])
                       
                    created_count += 1
