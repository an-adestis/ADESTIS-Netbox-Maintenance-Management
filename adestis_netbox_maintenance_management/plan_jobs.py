from datetime import date
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging
# from extras.jobs import Job
from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlans, MaintenanceTasks, Weekday

tasks = MaintenanceTasks.objects.all()
windows = MaintenanceTasks.objects.all()


def get_grouping_key_and_name(window):
    if window.recurrence_type == "weekly" and window.weekdays:
        # Mehrere Wochentage behandeln
        weekday_keys = window.weekdays.split(",") if isinstance(window.weekdays, str) else [window.weekdays]
        weekday_labels = []

        for key in weekday_keys:
            try:
                label = Weekday(key).label
                weekday_labels.append(label)
            except Exception:
                weekday_labels.append(f"Day {key}")

        label_str = ", ".join(weekday_labels)
        key_str = "_".join(weekday_keys)
        return f"weekly_{key_str}", f"Weekly Maintenance – {label_str}"

    elif window.recurrence_type == "monthly" and window.monthdays:
        return f"monthly_{window.monthdays.day}", f"Monthly Maintenance – Day {window.monthdays.day}"

    elif window.start_day:
        return f"date_{window.start_day}", f"One-time Maintenance – {window.start_day}"

    else:
        today = date.today()
        return f"date_{today}", f"Generated Maintenance Plan – {today}"


class AutoCreateMaintenancePlans(JobRunner):
    class Meta:
        name = "Automatically Generated Maintenance Plans"

    def run(self, *args, **kwargs):
        assigned_count = 0

        for task in MaintenanceTasks.objects.all():
            window = task.maintenance_windows
            if not window:
                continue

            grouping_key, plan_name = get_grouping_key_and_name(window)

            plan = MaintenancePlans.objects.get_or_create(
                grouping_key=grouping_key,
                defaults={'name': plan_name}
            )

            # Falls der Task noch nicht im Plan ist
            if not plan.tasks.filter(pk=task.pk).exists():
                plan.tasks.add(task)
                assigned_count += 1
    
    