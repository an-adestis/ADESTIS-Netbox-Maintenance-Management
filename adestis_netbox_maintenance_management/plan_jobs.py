from datetime import datetime, date, timedelta
from croniter import croniter
from cron_descriptor import get_description
import logging

from netbox.jobs import JobRunner
from adestis_netbox_maintenance_management.models import (
    MaintenanceTasks,
    MaintenancePlans,
)

logger = logging.getLogger(__name__)

task = MaintenanceTasks.objects.all()

WEEKDAY_MAP = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

def get_grouping_key_for_date(day) -> str:
    """Erzeugt einen eindeutigen Key für das Tagesdatum (nimmt auch Strings entgegen)."""
    if isinstance(day, str):
        try:
            day = datetime.fromisoformat(day).date()
        except ValueError:
            day = date.today()
    elif isinstance(day, datetime):
        day = day.date()
    elif isinstance(day, date):
        pass
    else:
        day = date.today()
    
    return f"date_{day.strftime('%Y%m%d')}"


def get_task_date(task):
    window = task.maintenance_windows
    if not window:
        return None

    # Cron-Ausdruck prüfen
    if window.special_ordinal:
        try:
            desc = get_description(window.special_ordinal)  # z. B. "Every minute, only on Monday"
            for day in WEEKDAY_MAP:
                if day.lower() in desc.lower():
                    return f"Weekday {day}"  # gleicher Key wie Weekly
            return f"cron {window.special_ordinal.strip()}"  # fallback
        except Exception:
            return f"cron {window.special_ordinal.strip()}"


    if window.recurrence_type == "daily":
        return "Daily"

    if window.recurrence_type == "weekly" and window.weekdays:
        if isinstance(window.weekdays, str):
            weekday_keys = [w.strip() for w in window.weekdays.split(",")]
        else:
            weekday_keys = [window.weekdays]
        return "_".join([f"Weekday {w}" for w in weekday_keys])


    if window.recurrence_type == "monthly" and getattr(window, "monthdays", None):
        day_num = getattr(window.monthdays, "day", None)
        month_num = getattr(window.monthdays, "month", None)  # falls vorhanden
        if day_num:
            key_parts = [f"Monthday {day_num}"]
            if month_num:
                key_parts.append(f"Month {month_num}")
            return "_".join(key_parts)


    if getattr(window, "start_day", None):
        return f"Date {window.start_day.isoformat()}"

    return None


class AutoCreateMaintenancePlans(JobRunner):
    class Meta:
        name = "Automatically Generated Maintenance Plans"

    def run(self, *args, **kwargs):
        assigned_count = 0
        grouped_tasks = {}

        for task in MaintenanceTasks.objects.select_related("maintenance_windows").all():
            window = task.maintenance_windows
            if not window:
                continue

            task_date_or_key = get_task_date(task)
            if not task_date_or_key:
                continue

            if isinstance(task_date_or_key, str):
                key = task_date_or_key
            elif isinstance(task_date_or_key, str) and task_date_or_key.startswith("Daily"):
                key = task_date_or_key
            else:
                key = get_grouping_key_for_date(task_date_or_key)
                
            grouped_tasks.setdefault(key, []).append(task)

        for key, tasks in grouped_tasks.items():
            
            if key.startswith("cron_"):
                    cron_expr = key[len("cron_"):]  # Cron-Teil extrahieren
                    try:
                        plan_name = get_description(cron_expr)
                    except Exception:
                            plan_name = cron_expr  # Fallback: roher Cron-String
            else:
                plan_name = f"Plan for Tasks {key}"

            plan, created = MaintenancePlans.objects.get_or_create(
                grouping_key=key,
                defaults={"name": plan_name},
            )

            for task in tasks:
                if not plan.maintenance_tasks.filter(pk=task.pk).exists():
                    plan.maintenance_tasks.add(task)
                    assigned_count += 1




