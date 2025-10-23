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


# -------------------------------------------------------
# 🔹 Hilfsfunktionen
# -------------------------------------------------------


def get_grouping_key_for_date(day) -> str:
    """Erzeugt einen eindeutigen Key für das Tagesdatum (nimmt auch Strings entgegen)."""
    if isinstance(day, str):
        try:
            day = datetime.fromisoformat(day).date()
        except ValueError:
            day = date.today()
    elif isinstance(day, datetime):
        day = day.date()
    return f"date_{day.strftime('%Y%m%d')}"


def get_task_date(task):
    """
    Gibt das relevante Ausführungsdatum eines Tasks zurück.
    Unterstützt: one-time, weekly, monthly, crontab (special_ordinal)
    """
    window = task.maintenance_windows
    if not window:
        return None

    now = datetime.now()

    if window.special_ordinal:
        # Cron-String als Schlüssel direkt nehmen
        return f"cron_{window.special_ordinal.strip()}"

    # 2️⃣ Wöchentlich
    if window.recurrence_type == "weekly" and window.weekdays:
        weekday_keys = (
            [int(k) for k in window.weekdays.split(",")]
            if isinstance(window.weekdays, str)
            else [window.weekdays]
        )
        today = now.date()
        days_ahead = min(((w - today.weekday()) % 7 for w in weekday_keys))
        return today + timedelta(days=days_ahead)

    # 3️⃣ Monatlich
    if window.recurrence_type == "monthly" and getattr(window, "monthdays", None):
        day_num = getattr(window.monthdays, "day", None)
        if day_num:
            today = now.date()
            try:
                return date(today.year, today.month, day_num)
            except ValueError:
                next_month = today.replace(day=1) + timedelta(days=31)
                return date(next_month.year, next_month.month, min(day_num, 28))

    # 4️⃣ Einmalig
    if getattr(window, "start_day", None):
        return window.start_day

    return None


# -------------------------------------------------------
# 🔹 Hauptjob
# -------------------------------------------------------

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

            if isinstance(task_date_or_key, str) and task_date_or_key.startswith("cron_"):
                key = task_date_or_key  # Cron-Ausdruck als Gruppierungs-Key
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
                plan_name = f"Plan für Gruppe {key}"

            plan, created = MaintenancePlans.objects.get_or_create(
                grouping_key=key,
                defaults={"name": plan_name},
            )

            for task in tasks:
                if not plan.maintenance_tasks.filter(pk=task.pk).exists():
                    plan.maintenance_tasks.add(task)
                    assigned_count += 1




