from datetime import datetime, date, timedelta
from croniter import croniter
from cron_descriptor import get_description
import logging

from netbox.jobs import JobRunner
from adestis_netbox_maintenance_management.models import (
    MaintenanceTasks,
    MaintenancePlans,
)
import re
from croniter import croniter

logger = logging.getLogger(__name__)

task = MaintenanceTasks.objects.all()

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
}

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
            # String in Datum konvertieren (ISO-Format)
            day = datetime.fromisoformat(day).date()
        except ValueError:
            # default: today
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

    # --- CRON-Logik ---
    if window.special_ordinal:
        try:
            # cron description
            desc = get_description(window.special_ordinal)  # z. B. "Every minute, only on Monday"
            
            # Prüfe, ob ein Wochentag im Beschreibungstext vorkommt
            for day in WEEKDAY_MAP:
                if day.lower() in desc.lower():
                    return f"Weekday {day}"  # gleicher Key wie Weekly
                
            month_match = re.search(r"day\s+(\d+).*only in\s+([a-z]+)", desc)
            if month_match:
                day_num = month_match.group(1)
                month_name = month_match.group(2)
                month_num = MONTH_MAP.get(month_name, date.today().month)
                return f"Monthday {day_num} Month {month_num}"

            # Prüfe auf 'on day X of the month' (ohne konkreten Monat)
            simple_month_match = re.search(r"day\s+(\d+)\s+of\s+the\s+month", desc)
            if simple_month_match:
                day_num = simple_month_match.group(1)
                # Füge aktuellen Monat hinzu, damit es mit normalen Monthly-Tasks übereinstimmt
                current_month = date.today().month
                return f"Monthday {day_num} Month {current_month}"
                
            return f"cron {desc}"  # fallback
        except Exception:
            return f"cron {desc}"


    if window.recurrence_type == "daily":
        return "Daily"

    if window.recurrence_type == "weekly" and window.weekdays:
        # Kann entweder ein String ("Monday, Tuesday") oder eine Liste sein
        
        label = f"Weekday {window.weekdays}"  # z. B. "Weekday Monday, Friday"
        if getattr(window, "week_in_month", None):
            label += f" ({window.get_week_in_month_display()})"  # z. B. "(First)"
        return label


    if window.recurrence_type == "monthly" and getattr(window, "monthdays", None):
        day_num = getattr(window.monthdays, "day", None)
        month_num = getattr(window.monthdays, "month", None)  # falls vorhanden
        if day_num and month_num:
            return f"Monthday {day_num} Month {month_num}"
            

    if getattr(window, "start_day", None):
        return f"Date {window.start_day.isoformat()}"

    return None


class AutoCreateMaintenancePlans(JobRunner):
    """
    JobRunner-Klasse, die automatisch Wartungspläne erstellt
    und Aufgaben anhand ihrer Zeitfenster gruppiert.
    """
    class Meta:
        name = "Automatically Generated Maintenance Plans"

    def run(self, *args, **kwargs):
        assigned_count = 0
        grouped_tasks = {}

        # Alle Wartungsaufgaben inkl. zugehörigem Zeitfenster laden
        for task in MaintenanceTasks.objects.select_related("maintenance_windows").all():
            window = task.maintenance_windows
            if not window:
                continue

            # Gruppierungskey oder Datum bestimmen
            task_date_or_key = get_task_date(task)
            logger.warning(f"Info: {task_date_or_key}")
            if not task_date_or_key:
                logger.warning("Zahl mal x das was wohl netbox maintenance")
                continue
                
            # Aufgaben nach Key gruppieren
            grouped_tasks.setdefault(task_date_or_key, []).append(task)

        # Jetzt für jede Gruppe einen Maintenance Plan anlegen oder aktualisieren
        for key, tasks in grouped_tasks.items():
            
            # Falls es sich um einen Cron-Ausdruck handelt
            if key.startswith("cron_"):
                cron_expr = key[len("cron_"):]  # Cron-Teil extrahieren
                try:
                    # Beschreibung des Cron-Ausdrucks als Planname
                    plan_name = get_description(cron_expr)
                except Exception:
                    plan_name = cron_expr  # Fallback: roher Cron-String
            else:
                # Standardname für Plan
                plan_name = f"Plan for Tasks {key}"

            # Wartungsplan anhand des Gruppierungsschlüssels erstellen oder abrufen
            plan, created = MaintenancePlans.objects.get_or_create(
                grouping_key=key,
                defaults={"name": plan_name},
            )

            # Alle Aufgaben dieser Gruppe dem Plan zuordnen
            for task in tasks:
                if not plan.maintenance_tasks.filter(pk=task.pk).exists():
                    plan.maintenance_tasks.add(task)
                    assigned_count += 1



