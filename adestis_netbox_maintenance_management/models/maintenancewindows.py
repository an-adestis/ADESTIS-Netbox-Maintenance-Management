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
from django.core.validators import MinValueValidator, MaxValueValidator


__all__ = (
    'MaintenanceWindows',
    'Weekday',
    'ScheduleTypeModeChoices',
    'RecurrenceTypeChoices'
)
class RecurrenceTypeChoices(ChoiceSet):

        SELECT = 'select'
        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'
        Special_Ordinal = 'special_ordinal'
        

        CHOICES = [
            (SELECT, 'Select'),
            (DAILY, 'Daily'),
            (WEEKLY, 'Weekly'),
            (MONTHLY, 'Monthly'),
            (Special_Ordinal, 'Cron Tab'),
            
        ]
        
        
DAY_CHOICES = [
    (1, "1st"), (2, "2nd"), (3, "3rd"), (4, "4th"), (5, "5th"),
    (6, "6th"), (7, "7th"), (8, "8th"), (9, "9th"), (10, "10th"),
    (11, "11th"), (12, "12th"), (13, "13th"), (14, "14th"), (15, "15th"),
    (16, "16th"), (17, "17th"), (18, "18th"), (19, "19th"), (20, "20th"),
    (21, "21st"), (22, "22nd"), (23, "23rd"), (24, "24th"), (25, "25th"),
    (26, "26th"), (27, "27th"), (28, "28th"), (29, "29th"), (30, "30th"),
    (31, "31st"),
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
        
class ScheduleTypeModeChoices(ChoiceSet):

        key = 'schedule_type_mode'

        SELECT = 'select'
        RECURRING = 'recurring'
        ONE_TIME = 'one_time'

        CHOICES = [
            (SELECT, _('Select')),
            (RECURRING, _('Recurring')),
            (ONE_TIME, _('One-time')),
        ]
    
class MaintenanceWindows(NetBoxModel):
    
    week_in_month = django_models.IntegerField(
        choices=[
            (1, "First"),
            (2, "Second"),
            (3, "Third"),
            (4, "Fourth"),
            (5, "Last"),  # 5 wird als "Last" interpretiert
            (6, "Every"),
        ],
        blank = True,
        null = True
    )

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
        
    schedule_type = django_models.CharField(max_length=20, choices=ScheduleTypeModeChoices, null=False, blank=False, default=ScheduleTypeModeChoices.SELECT)
    
    start_day = django_models.DateField(
        blank=True,
        null=True,
    )
    
    end_day = django_models.DateField(
        blank=True,
        null=True,
    )

    recurrence_type = django_models.CharField(
        max_length=20,
        choices=RecurrenceTypeChoices,
        default=RecurrenceTypeChoices.SELECT,
        blank=True,
        null=True
    )
    
    weekdays = django_models.CharField(
        max_length=50, 
        choices=Weekday.CHOICES,
        blank=True,
        null=True,
        help_text="Weekly"
    )

    monthdays = django_models.DateField(
        blank=True,
        null=True,
        verbose_name=("First Execution")
    )
    
    day_of_month = django_models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Day of Month",
        help_text="Specify the day of the month for monthly recurrence",
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        choices=DAY_CHOICES
    )

    special_ordinal = django_models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=""
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
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'windows_tenant',
         null = True,
         verbose_name='Tenant',
         blank = True
    )
    
    class Meta:
        verbose_name_plural = "Maintenance Windows"
        verbose_name = 'Maintenance Window'
        ordering = ('name',)

    def clean_week_in_month(self):
        value = self.cleaned_data.get('week_in_month')
        if value == '':
            return None
        return value

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenancewindows', args=[self.pk])

    def __str__(self):
        return self.name 