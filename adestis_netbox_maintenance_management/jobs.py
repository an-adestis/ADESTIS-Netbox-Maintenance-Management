from datetime import date
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging
# from extras.jobs import Job
from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlannedActions, MaintenanceTasks, TaskStatusChoices
from cron_descriptor import get_description, ExpressionDescriptor
from adestis_netbox_maintenance_management.plan_jobs import is_task_due_today, is_task_due_in_future

logger = logging.getLogger(__name__)

@system_job(interval=JobIntervalChoices.INTERVAL_MINUTELY)
class AutoCreateMaintenanceTasks(JobRunner):
    class Meta:
        name = "Automatically Generated Maintenance Tasks"
        

    def run(self, *args, **kwargs):
        today = date.today()
        created_count = 0
        skipped_count = 0

        windows = MaintenanceWindows.objects.all()

        for window in windows:
            actions = MaintenanceActions.objects.filter(maintenance_window=window).all()

            for action in actions:
                logger.error(f"Tasks Job wurde ausgeführt")

                # maintenance_tasks = MaintenanceTasks.objects.filter(maintenance_action=action).first()

                     
                # Prüfen, ob für diese Action bereits ein Task existiert
                task = MaintenanceTasks.objects.filter(
                    maintenance_action=action
                ).first()

                # Wenn kein Task existiert → neuen erstellen
                if not task:

                    schedule_label = (
                        str(window.start_day or window.weekdays or window.day_of_month or "Schedule")
                    )

                    if schedule_label.lower() in window.name.lower():
                        task_name = window.name
                    else:
                        task_name = f"{window.name} {schedule_label}"

                    task = MaintenanceTasks.objects.create(
                        name=task_name,
                        status=TaskStatusChoices.STATUS_PLANNED,  # Standard
                        maintenance_action=action,
                        maintenance_windows=window,
                        comments=action.comments,
                    )

                    # Beziehungen setzen
                    task.virtual_machine.set(action.virtual_machine.all())
                    task.device.set(action.device.all())

                    created_count += 1

                # --- Status setzen ---
                new_status = None

                if is_task_due_today(task):
                    new_status = TaskStatusChoices.STATUS_ACTIVE
                elif is_task_due_in_future(task):
                    new_status = TaskStatusChoices.STATUS_PLANNED
                else:
                    new_status = TaskStatusChoices.STATUS_ARCHIVED

                # Nur speichern, wenn wirklich geändert
                if task.status != new_status:
                    task.status = new_status
                    task.save()