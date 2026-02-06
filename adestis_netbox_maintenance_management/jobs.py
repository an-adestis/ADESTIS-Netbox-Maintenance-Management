from datetime import datetime, time, timedelta
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging

from datetime import datetime, date, timedelta
from django.utils import timezone

from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlannedActions, MaintenanceTasks, TaskStatusChoices
from cron_descriptor import get_description, ExpressionDescriptor
from adestis_netbox_maintenance_management.plan_jobs import is_task_due_today, is_task_due_in_future

logger = logging.getLogger(__name__)


@system_job(interval=JobIntervalChoices.INTERVAL_MINUTELY)
class AutoCreateMaintenanceTasks(JobRunner):
    class Meta:
        name = "Automatically Generated Maintenance Tasks"

    def run(self, *args, **kwargs):
        now = datetime.now().time()
        if not (time(8, 0) <= now <= time(18, 0)):
            return

        logger = logging.getLogger(__name__)
        logger.error("Tasks Job gestartet")

        windows = MaintenanceWindows.objects.all()

        for window in windows:
            actions = MaintenanceActions.objects.filter(
                maintenance_window=window
            )

            for action in actions:

                # Wenn Action bereits ARCHIVED Tasks hat -> Action sofort löschen
                # (so wird verhindert, dass sie wieder einen Task erzeugt)
                archived_tasks_for_action = MaintenanceTasks.objects.filter(
                    maintenance_action=action,
                    status=TaskStatusChoices.STATUS_ARCHIVED
                )

                if archived_tasks_for_action.exists():
                    logger.error(f"Action {action.id} hat ARCHIVED Tasks -> lösche Action + Tasks")
                    archived_tasks_for_action.delete()
                    action.delete()
                    continue

                # Task für diese Action holen (wenn vorhanden)
                task = MaintenanceTasks.objects.filter(
                    maintenance_action=action
                ).order_by("-id").first()

                # Wenn Task existiert und nicht ARCHIVED ist -> nix tun
                if task and task.status != TaskStatusChoices.STATUS_ARCHIVED:
                    continue

                # Wenn kein Task existiert -> erstellen
                if not task:
                    task = MaintenanceTasks.objects.create(
                        name=f"{window.name}",
                        status=TaskStatusChoices.STATUS_PLANNED,
                        maintenance_action=action,
                        maintenance_windows=window,
                        comments=action.comments,
                    )
                    task.virtual_machine.set(action.virtual_machine.all())
                    task.device.set(action.device.all())
                    logger.error(f"Action {action.id} -> Task {task.id} erstellt")

                # Status Update
                if is_task_due_today(task):
                    new_status = TaskStatusChoices.STATUS_ACTIVE
                elif is_task_due_in_future(task):
                    new_status = TaskStatusChoices.STATUS_PLANNED
                else:
                    new_status = TaskStatusChoices.STATUS_ARCHIVED

                if task.status != new_status:
                    task.status = new_status
                    task.save()
                    logger.error(f"Task {task.id} status updated to {new_status}")

                # Wenn ARCHIVED -> Task + Action löschen
                if task.status == TaskStatusChoices.STATUS_ARCHIVED:
                    logger.error(f"Task {task.id} ist ARCHIVED -> lösche Task + Action")
                    action.delete()
                    task.delete()

        # Cleanup: ARCHIVED Tasks löschen, wenn älter als 7 Tage
        # ACHTUNG: Du hast kein Datumfeld -> geht nur, wenn du ein Feld hast.
        # Wenn nicht vorhanden, wird das hier NICHT funktionieren.
        #
        # Wenn du kein Datumfeld willst, kommentiere den Cleanup aus.

        logger.error("Job erfolgreich beendet")

