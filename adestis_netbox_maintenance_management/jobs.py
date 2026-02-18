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


@system_job(interval=3)
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
                cutoff = timezone.now() - timedelta(minutes=1)
                if hasattr(action, "created") and action.created < cutoff:

                    tasks = MaintenanceTasks.objects.filter(maintenance_action=action)

                    if tasks.filter(status=TaskStatusChoices.STATUS_ARCHIVED).exists():
                        tasks.delete()
                        action.delete()

                        continue

                task = MaintenanceTasks.objects.filter(
                    maintenance_action=action
                ).order_by("-id").first()

                if task and task.status == TaskStatusChoices.STATUS_ARCHIVED:
                    continue

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

                if is_task_due_today(task):
                    new_status = TaskStatusChoices.STATUS_ACTIVE
                elif is_task_due_in_future(task):
                    new_status = TaskStatusChoices.STATUS_PLANNED
                else:
                    new_status = TaskStatusChoices.STATUS_ARCHIVED

                if task.status != new_status:
                    task.status = new_status
                    task.save()