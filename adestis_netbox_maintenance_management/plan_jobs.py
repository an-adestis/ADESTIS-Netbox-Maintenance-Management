from datetime import datetime, date, timedelta
import json
from croniter import croniter
from cron_descriptor import get_description
import logging

from netbox.jobs import JobRunner
from adestis_netbox_maintenance_management.models import (
    MaintenanceTasks,
    MaintenancePlannedActions,
    TaskStatusChoices
)
import re
from croniter import croniter
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job

logger = logging.getLogger(__name__)

# task = MaintenanceTasks.objects.all()

MONTH_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
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

    # try:
    #     # logger.error("Type: "+type(task).__name__)
    #     logger.error(task.__dict__)

    #     window = task.maintenance_windows
    #     logger.warning(f"Window: {window}")
    # except Exception as e:
    #     logger.error(f"ERROR in window: {e!r}")
    logger.error(task)
    logger.error(task.__dict__)
    window = task.maintenance_windows
    logger.warning(f"Window: {window}")
    # --- CRON-Logik ---
    if window.special_ordinal:
        try:
            # cron description
            desc = get_description(window.special_ordinal)  # z. B. "Every minute, only on Monday"
            
            # Prüfe, ob ein Wochentag im Beschreibungstext vorkommt
            for day in WEEKDAY_MAP:
                if day.lower() in desc.lower():
                    return f"Weekday {day}"  # gleicher Key wie Weekly
                
            month_match = re.search(r"day\s+(\d+).*?only in\s+([a-zA-Z]+)", desc)
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


    if window.recurrence_type == "monthly":
        if getattr(window, "day_of_month", None):
            # Verwende das aktuelle Monat, wenn kein month-Feld gesetzt ist
            current_month = date.today().month
            return f"Monthday {window.day_of_month} Month {current_month}"
        elif getattr(window, "monthdays", None):
            day_num = getattr(window.monthdays, "day", None)
            month_num = getattr(window.monthdays, "month", date.today().month)
            return f"Monthday {day_num} Month {month_num}"
            

    if getattr(window, "start_day", None):
        return f"Date {window.start_day.isoformat()}"

    return None

def is_task_due_today(task):
    """Prüft, ob ein Task heute fällig ist."""
    today = date.today()
    today_weekday = today.weekday()
    today_day = today.day
    today_month = today.month

    key = get_task_date(task)
    logger.warning(f"Logger Key:{key}")
    if not key:
        return False

    if key.startswith("date_"):
        key_date = datetime.strptime(key.replace("date_", ""), "%Y%m%d").date()
        return key_date == today

    elif key.startswith("Weekday"):
        for day_name, wd_index in WEEKDAY_MAP.items():
            if day_name in key and wd_index == today_weekday:
                return True

    elif key.startswith("Monthday"):
        parts = key.split()
        day_num = int(parts[1])
        month_num = int(parts[3])
        return day_num == today_day and month_num == today_month

    elif key.startswith("cron"):
        cron_expr = task.maintenance_windows.special_ordinal
        try:
            ci = croniter(cron_expr, today)
            return ci.get_next(datetime).date() == today
        except Exception:
            return False
        
    elif key.startswith("Date"):
        # Erwartetes Format: "Date 2025-11-14"
        try:
            date_str = key.replace("Date ", "").strip()
            key_date = datetime.fromisoformat(date_str).date()
            return key_date == today
        except ValueError:
            logger.warning(f"Ungültiges Datumsformat im Key: {key}")
            return False

    return False

@system_job(interval=JobIntervalChoices.INTERVAL_MINUTELY)
class AutoCreateMaintenancePlannedActions(JobRunner):
    """
    JobRunner-Klasse, die automatisch Wartungspläne erstellt
    und Aufgaben anhand ihrer Zeitfenster gruppiert.
    """
    class Meta:
        name = "Automatically Generated Planned Actions"

    def run(self, *args, **kwargs):
        assigned_count = 0
        grouped_tasks = {}
        
        for plan in MaintenancePlannedActions.objects.filter(grouping_key="Today"):
            plan.maintenance_tasks.clear()

        # Alle Wartungsaufgaben inkl. zugehörigem Zeitfenster laden
        tasks = MaintenanceTasks.objects.select_related("maintenance_windows").all()
        logger.error(f"Tasks:{tasks}")
        for task in tasks:
            window = task.maintenance_windows
            logger.error(f"Fancy task: {task}")
            logger.error(f"Fancy window: {window}")
            if not window:
                continue
            # Gruppierungskey oder Datum bestimmen
            task_date_or_key = get_task_date(task)
            
            
            due_today = is_task_due_today(task)

            
            if not task_date_or_key:
                continue
            
            dictionary_key = task_date_or_key
            if due_today == True:
                dictionary_key = "Today"
                
            # Aufgaben nach Key gruppieren
            grouped_tasks.setdefault(dictionary_key, []).append(task)

        # Jetzt für jede Gruppe einen Maintenance Plan anlegen oder aktualisieren
        for key, tasks in grouped_tasks.items():

            # Wenn nach dem Filtern keine Tasks mehr übrig sind → Plan gar nicht erstellen
            if not tasks:
                continue
            
            plan_name = f"Plan for Tasks {key}"

            # Wartungsplan anhand des Gruppierungsschlüssels erstellen oder abrufen
            plan, created = MaintenancePlannedActions.objects.get_or_create(
                grouping_key=key,
                defaults={"name": plan_name},
            )
            
            plan.maintenance_tasks.set(tasks)
            assigned_count += len(tasks)