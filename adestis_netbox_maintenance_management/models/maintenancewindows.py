from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import VirtualMachine
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.postgres.fields import ArrayField 
from datetime import timedelta
from crontab import CronTab


__all__ = (
    'MaintenanceWindows',
    'Weekday',
    'ScheduleTypeModeChoices',
    'RecurrenceTypeChoices',
    'Weekday',
)
class RecurrenceTypeChoices(ChoiceSet):

        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'
        WEEKDAY_OCCURRENCE = 'weekday_occurrence'
        WORKDAY_OCCURRENCE = 'workday_occurrence'

        CHOICES = [
            (DAILY, 'Daily'),
            (WEEKLY, 'Weekly'),
            (MONTHLY, 'Monthly'),
            (WEEKDAY_OCCURRENCE, 'x.  weekday of the month'),
            (WORKDAY_OCCURRENCE, 'x. workday of the month'),
        ]
class Weekday(ChoiceSet):
        key = 'weekday'
        
        MON = 'Monday'
        TUE = 'Tuesday'
        WED = 'Wednesday'
        THU = 'Thursday'
        FRI = 'Friday'
        SAT = 'Saturday'
        SUN = 'Sunday'

        CHOICES = [
            (MON, 'Monday'),      
            (TUE, 'Tuesday'),     
            (WED, 'Wednesday'),   
            (THU, 'Thursday'),    
            (FRI, 'Friday'),      
            (SAT, 'Saturday'),    
            (SUN, 'Sunday'),      
        ]
        
class Workday(ChoiceSet):
        key = 'weekday'
        
        MON = 'monday'
        TUE = 'tuesday'
        WED = 'wednesday'
        THU = 'thursday'
        FRI = 'friday'

        CHOICES = [
            (MON, 'Monday'),      
            (TUE, 'Tuesday'),     
            (WED, 'Wednesday'),   
            (THU, 'Thursday'),    
            (FRI, 'Friday'),            
        ]
        
class ScheduleTypeModeChoices(ChoiceSet):

        key = 'schedule_type_mode'

        SELECT_File = 'select'
        RECURRING = 'recurring'
        ONE_TIME = 'one_time'

        CHOICES = [
            (SELECT_File, 'Select'),
            (RECURRING, _('Recurring')),
            (ONE_TIME, _('One-time')),
        ]
    
class MaintenanceWindows(NetBoxModel):

    comments = django_models.TextField(
        blank=True
    )
    
    name = django_models.CharField(
        max_length=150
    )
    
    description = django_models.CharField(
        max_length=500,
        blank = True
    )
        
    schedule_type = django_models.CharField(max_length=20, choices=ScheduleTypeModeChoices, null=False, blank=False, default=ScheduleTypeModeChoices.SELECT_File)
    
    start_day = django_models.DateField(
        blank=True,
        null=True,
    )
    
    end_day = django_models.DateField(
        blank=True,
        null=True,
    )

    recurrence_type =django_models.CharField(
        max_length=20,
        choices=RecurrenceTypeChoices,
        default=RecurrenceTypeChoices.DAILY,
        blank=True,
        null=True
    )
    
    weekdays =django_models.CharField(
        max_length=50, 
        choices=Weekday.CHOICES,
        blank=True,
        null=True,
        help_text="Weekly"
    )

    monthdays = django_models.DateField(
        blank=True,
        null=True,
    )

    special_ordinal = django_models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="* 9 * * 1 `09:00 Monday`"
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        verbose_name='Virtual Machines',
        related_name='maintenance_window',
        blank = True
    )
    
    start_time = django_models.TimeField(
        blank=True, 
        null = True,
    )
    
    end_time = django_models.TimeField(
        blank= True, 
        null=True,
    )
    
    class Meta:
        verbose_name_plural = "Maintenance Windows"
        verbose_name = 'Maintenance Window'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenancewindows', args=[self.pk])

    def __str__(self):
        return self.name 