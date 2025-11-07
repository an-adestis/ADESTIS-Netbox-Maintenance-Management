from datetime import date
from django.db.models import Q
from core.choices import JobIntervalChoices
from netbox.jobs import JobRunner, system_job
import logging
# from extras.jobs import Job
from adestis_netbox_maintenance_management.models import MaintenanceWindows, MaintenanceActions, MaintenancePlans, MaintenanceTasks
from cron_descriptor import get_description, ExpressionDescriptor

logger = logging.getLogger(__name__)

class AutoCreateMaintenanceTasks(JobRunner):
    class Meta:
        name = "Automatically Generated Maintenance Tasks"
        # model = MaintenancePlans

    def run(self, *args, **kwargs):
        
        # get date values for today 
        today = date.today()
        # weekday = today.weekday()  # Montag = 0

        
        # create a new Plan
        created_count = 0
        # skip already existing Plans
        skipped_count = 0

        windows = MaintenanceWindows.objects.all()
        
        def get_schedule_label_or_today(window):
            fields = [
                window.start_day,
                window.end_day,
                window.weekdays,
                window.week_in_month,
                window.monthdays,
                window.day_of_month,
                window.start_time,
                window.end_time,
                window.recurrence_type,
            ]
            
            if window.weekdays:
                label = str(window.weekdays)  # nur weekdays als String
                if window.week_in_month:
                    label += f" ({window.get_week_in_month_display()})"
                return label
            
            if window.monthdays:
                # Einfach den Tag als Zahl nehmen und als String anhängen
                label = str(window.monthdays.day)
                
                # Wenn day_of_month gesetzt ist (ChoiceField), einfach den Text anhängen
                if window.day_of_month:
                    label += f" ({window.get_day_of_month_display()})"
                
                return label

            
            cron_expr = window.special_ordinal
            if cron_expr:
                try:
                    description = get_description(cron_expr)
                    return description
                except Exception:
                    return cron_expr

            for value in fields:
                if value:
                    return str(value)  # Konvertieren zu String

            return str(date.today())
        
        
        for window in windows:
            actions = MaintenanceActions.objects.filter(maintenance_window=window).all()

            

            for action in actions:
                
                
                    
                if not MaintenanceTasks.objects.filter(maintenance_action=action).exists():
                    
                        schedule_label = get_schedule_label_or_today(window)

                        # Prüfen, ob das Label schon im Window-Namen steht
                        if schedule_label.lower() in window.name.lower():
                            task_name = window.name
                        else:
                            task_name = f"{window.name} {schedule_label}"
                            
                        task = MaintenanceTasks.objects.create(
                            name = task_name,
                            maintenance_action=action, 
                            maintenance_windows = window,
                            comments = action.comments
                        )
                        task.virtual_machine.set(action.virtual_machine.all())
                        task.device.set(action.device.all())
                        created_count += 1
