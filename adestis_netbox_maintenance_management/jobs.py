from datetime import date
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging
# from extras.jobs import Job
from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlannedActions, MaintenanceTasks, TaskStatusChoices
from cron_descriptor import get_description, ExpressionDescriptor
from adestis_netbox_maintenance_management.plan_jobs import is_task_due_today

logger = logging.getLogger(__name__)



class AutoCreateMaintenanceTasks(JobRunner):
    class Meta:
        name = "Automatically Generated Maintenance Tasks"
        

    def run(self, *args, **kwargs):
        today = date.today()
        created_count = 0
        skipped_count = 0

        windows = MaintenanceWindows.objects.all()
        
        # logger.error(f"Test:{windows}")

        for window in windows:
            actions = MaintenanceActions.objects.filter(maintenance_window=window).all()

            for action in actions:

                maintenance_tasks = MaintenanceTasks.objects.filter(maintenance_action=action).first()

                if maintenance_tasks:
                    if not is_task_due_today(maintenance_tasks):
                        maintenance_tasks.status = TaskStatusChoices.STATUS_ARCHIVED
                        maintenance_tasks.save()
                    else:
                        maintenance_tasks.status = TaskStatusChoices.STATUS_ACTIVE
                        maintenance_tasks.save()
                    continue
                    

                # Taskname erstellen
                schedule_label = str(window.start_day or window.weekdays or window.day_of_month or "Schedule")
                if schedule_label.lower() in window.name.lower():
                    task_name = window.name
                else:
                    task_name = f"{window.name} {schedule_label}"

                # Task erstellen
                task = MaintenanceTasks.objects.create(
                    name=task_name,
                    status=TaskStatusChoices.STATUS_ACTIVE,
                    maintenance_action=action,
                    maintenance_windows=window,
                    comments=action.comments
                )

                # VM/Device Beziehungen setzen
                task.virtual_machine.set(action.virtual_machine.all())
                task.device.set(action.device.all())

                created_count += 1