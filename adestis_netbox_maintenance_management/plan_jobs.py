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

from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job

logger = logging.getLogger(__name__)
import calendar
from typing import Optional

from tenancy.models import *
from dcim.models import *
from virtualization.models import *

from django.utils.safestring import mark_safe

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
    """
    Liefert den Scheduling-Key für eine Task zurück:
    - cron
    - Weekday
    - Monthday
    - Daily
    - Date
    """
    window = task.maintenance_windows
    if not window:
        return None

    if getattr(window, "special_ordinal", None):
        try:
            cron_expr = window.special_ordinal
            description = get_description(cron_expr) 
            return f"cron {description}"
        except Exception:
            return f"cron {window.special_ordinal}"

    if getattr(window, "recurrence_type", None) == "weekly" and getattr(window, "weekdays", None):
        return f"Weekday {window.weekdays}"

    if getattr(window, "recurrence_type", None) == "monthly":
        if getattr(window, "day_of_month", None):
            current_month = date.today().month
            return f"Monthday {window.day_of_month} Month {current_month}"

    if getattr(window, "recurrence_type", None) == "daily":
        return "Daily"

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
        cron_expr = key.replace("cron ", "").strip()
        try:
            start_of_day = datetime.combine(today, datetime.min.time())
            end_of_day = datetime.combine(today, datetime.max.time())

            ci = croniter(cron_expr, start_of_day - timedelta(seconds=1))

            while True:
                next_run = ci.get_next(datetime)

                if next_run > end_of_day:
                    return False

                if start_of_day <= next_run <= end_of_day:
                    return True

        except Exception:
            return False

        
    elif key.startswith("Date"):
        try:
            date_str = key.replace("Date ", "").strip()
            key_date = datetime.fromisoformat(date_str).date()
            return key_date == today
        except ValueError:
            return False

    return False


def is_task_due_in_future(task, return_date=False):
    """Prüft, ob ein Task in der Zukunft fällig ist oder gibt das nächste Datum zurück."""
    today = date.today()
    key = get_task_date(task)
    now = datetime.now()
    week_in_month = task.maintenance_windows.week_in_month
    
    

    if not key:
        return None if return_date else False

    if key.startswith("date_"):
        key_date = datetime.strptime(key.replace("date_", ""), "%Y%m%d").date()
        if return_date:
            return key_date
        return key_date > today

    elif key.startswith("Weekday"):
        target_weekday = next(
            (WEEKDAY_MAP[day_name] for day_name in WEEKDAY_MAP if day_name in key),
            None
        )
        if target_weekday is None:
            return None if return_date else False

        if week_in_month:
            year = today.year
            month = today.month

            if week_in_month == 6:
                next_date = today + timedelta((target_weekday - today.weekday() + 7) % 7)

            elif week_in_month == 5:
                if month < 12:
                    last_day = date(year, month + 1, 1) - timedelta(days=1)
                else:
                    last_day = date(year, 12, 31)

                day_diff = (last_day.weekday() - target_weekday) % 7
                next_date = last_day - timedelta(days=day_diff)

            else:
                first_day = date(year, month, 1)
                first_target = first_day + timedelta(
                    (target_weekday - first_day.weekday() + 7) % 7
                )
                next_date = first_target + timedelta(weeks=week_in_month - 1)

        else:
            next_date = today + timedelta(
                (target_weekday - today.weekday() + 7) % 7
            )

        if return_date:
            return next_date
        return next_date > today

    elif key.startswith("Monthday"):
        parts = key.split()
        day_num = int(parts[1])
        month_num = int(parts[3])
        key_date = date(today.year, month_num, day_num)

        if return_date:
            return key_date
        return key_date > today

    elif key.startswith("cron"):
        cron_expr = task.maintenance_windows.special_ordinal
        try:
            ci = croniter(cron_expr, now)
            next_run = ci.get_next(datetime)
            next_date = next_run.date()

            if return_date:
                return next_date

            return next_date > today

        except Exception:
            return None if return_date else False

    elif key.startswith("Daily"):
        if return_date:
            return today
        return True

    elif key.startswith("Date"):
        try:
            date_str = key.replace("Date ", "").strip()
            key_date = datetime.fromisoformat(date_str).date()
            if return_date:
                return key_date
            return key_date > today
        except ValueError:
            return None if return_date else False

    return None if return_date else False

@system_job(interval=5)
class AutoCreateMaintenancePlannedActions(JobRunner):
    class Meta:
        name = "Automatically Generated Planned Actions"

    def run(self, *args, **kwargs):
        assigned_count = 0
        grouped_tasks = {}
        
        for plan in MaintenancePlannedActions.objects.filter(grouping_key="Today"):
            plan.maintenance_tasks.clear()

        tasks = MaintenanceTasks.objects.select_related("maintenance_windows").all()
        
        logger.error("Job wurde ausgeführt")
        for task in tasks:
            window = task.maintenance_windows
            if not window:
                continue
            task_date_or_key = get_task_date(task)
            
            due_today = is_task_due_today(task)
            
            if not task_date_or_key:
                continue
            
            dictionary_key = task_date_or_key
            if due_today == True:
                dictionary_key = "Today"
                
            grouped_tasks.setdefault(dictionary_key, []).append(task)

        for key, tasks in grouped_tasks.items():
            
            all_archived = all(task.status == TaskStatusChoices.STATUS_ARCHIVED for task in tasks)

            if all_archived:
                continue  
            
            plan_name = f"Plan for Tasks {key}"
            plan, created = MaintenancePlannedActions.objects.get_or_create(
                grouping_key=key,
                defaults={"name": plan_name},
            )
            
            plan.maintenance_tasks.set(tasks)

            plan.virtual_machine.set(
                VirtualMachine.objects.filter(id__in=[vm.id for task in tasks for vm in task.virtual_machine.all()])
            )
            plan.device.set(
                Device.objects.filter(id__in=[dev.id for task in tasks for dev in task.device.all()])
            )

            plan.save()

            assigned_count += len(tasks)

        plans = MaintenancePlannedActions.objects.prefetch_related("maintenance_tasks")

        for plan in plans:
            
            archived_tasks = plan.maintenance_tasks.filter(
                status=TaskStatusChoices.STATUS_ARCHIVED
            )
            if archived_tasks.exists():
                plan.maintenance_tasks.remove(*archived_tasks)

            if plan.maintenance_tasks.count() == 0:
                plan.delete()