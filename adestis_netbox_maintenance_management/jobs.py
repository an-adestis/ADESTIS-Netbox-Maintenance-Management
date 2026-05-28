from datetime import datetime, time, timedelta
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging

from datetime import datetime, date, timedelta
from django.utils import timezone

from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlannedActions, MaintenanceTasks, TaskStatusChoices
from cron_descriptor import get_description, ExpressionDescriptor
from adestis_netbox_maintenance_management.plan_jobs import is_task_due_today, is_task_due_in_future, get_task_date, WEEKDAY_MAP
from croniter import croniter
logger = logging.getLogger(__name__)


def get_next_due_date(task):
    """Berechnet das nächste Fälligkeitsdatum oder None."""
    today = date.today()
    key = get_task_date(task)
    now = datetime.now()
    week_in_month = task.maintenance_windows.week_in_month

    if not key:
        return None


    if key.startswith("date_"):
        return datetime.strptime(
            key.replace("date_", ""), "%Y%m%d"
        ).date()


    elif key.startswith("Weekday"):
        target_weekday = next(
            (WEEKDAY_MAP[d] for d in WEEKDAY_MAP if d in key),
            None
        )
        if target_weekday is None:
            return None


        if week_in_month:
            year = today.year
            month = today.month

            if week_in_month == 6:
                delta = (target_weekday - today.weekday() + 7) % 7
                return today + timedelta(days=delta)

            elif week_in_month == 5:
                if month < 12:
                    last_day = date(year, month + 1, 1) - timedelta(days=1)
                else:
                    last_day = date(year, 12, 31)

                day_diff = (last_day.weekday() - target_weekday) % 7
                return last_day - timedelta(days=day_diff)

            else:
                first_day = date(year, month, 1)
                first_target = first_day + timedelta(
                    (target_weekday - first_day.weekday() + 7) % 7
                )
                return first_target + timedelta(weeks=week_in_month - 1)

        else:
            delta = (target_weekday - today.weekday() + 7) % 7
            return today + timedelta(days=delta)


    elif key.startswith("Monthday"):
        parts = key.split()
        day_num = int(parts[1])
        month_num = int(parts[3])
        return date(today.year, month_num, day_num)


    elif key.startswith("cron"):
        cron_expr = task.maintenance_windows.special_ordinal
        try:
            ci = croniter(cron_expr, now)
            next_run = ci.get_next(datetime)
            return next_run.date()

        except Exception as e:
            print(f"Ungültiger Cron '{cron_expr}': {e}")
            return None

    elif key.startswith("Daily"):
        return today


    elif key.startswith("Date"):
        try:
            date_str = key.replace("Date ", "").strip()
            return datetime.fromisoformat(date_str).date()
        except ValueError:
            return None

    return None

@system_job(interval=2)
class AutoCreateMaintenanceTasks(JobRunner):
    class Meta:
        name = "Automatically Generated Maintenance Tasks"

    def run(self, *args, **kwargs):

        logger = logging.getLogger(__name__)
        logger.error("Tasks Job gestartet")

        windows = MaintenanceWindows.objects.all()

        for window in windows:
            actions = MaintenanceActions.objects.filter(
                maintenance_window=window
            )

            for action in actions:
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
                    task.virtual_machine.set(
                        action.virtual_machine.all() if getattr(action, "virtual_machine", None) else []
                    )

                    task.device.set(
                        action.device.all() if getattr(action, "device", None) else []
                    )
                    
                    task.tenant = action.tenant if getattr(action, "tenant", None) else None

                    task.save()
                    
                today = date.today()
                next_due = get_next_due_date(task)
        

                if is_task_due_today(task):
                    new_status = TaskStatusChoices.STATUS_ACTIVE
                elif is_task_due_in_future(task):
                    new_status = TaskStatusChoices.STATUS_PLANNED
                else:
                    new_status = TaskStatusChoices.STATUS_ARCHIVED
                    
                if task.status != new_status or task.next_due_date != next_due:
                    task.status = new_status
                    task.next_due_date = next_due
                    task.save()