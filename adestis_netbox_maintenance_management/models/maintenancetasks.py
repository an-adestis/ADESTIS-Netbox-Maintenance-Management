from django.db import models as django_models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from tenancy.models import *
from dcim.models import *
from virtualization.models import *
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.postgres.fields import ArrayField 
from datetime import timedelta
from adestis_netbox_maintenance_management.models import MaintenanceActions
from core.choices import JobIntervalChoices

from django.utils import timezone
from datetime import timedelta

__all__ = (
    'MaintenanceTasks',
    'TaskStatusChoices',
)

class TaskStatusChoices(ChoiceSet):
    key = 'MaintenanceTasks.status'

    STATUS_ACTIVE = 'active'
    STATUS_ARCHIVED = 'archived'
    STATUS_PLANNED = 'planned'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_ARCHIVED, 'Archived', 'red'),
        (STATUS_PLANNED, 'Planned', 'blue'),
    ]

class MaintenanceTasks(NetBoxModel):

    comments = django_models.TextField(
        blank=True
    )
    
    status = django_models.CharField(
        max_length=50,
        choices=TaskStatusChoices,
        verbose_name='Status',
        help_text='Status'
    )
    
    name = django_models.CharField(
        max_length=150
    )
    
    description = django_models.CharField(
        max_length=500,
        blank = True
    )
    
    maintenance_action = django_models.ForeignKey(
        to='adestis_netbox_maintenance_management.MaintenanceActions',
        on_delete= django_models.PROTECT,
        related_name='task_maintenance_actions',
        blank=False,
        null=False
    )
    
    maintenance_windows = django_models.ForeignKey(
        to='adestis_netbox_maintenance_management.MaintenanceWindows',
        on_delete= django_models.PROTECT,
        related_name='task_maintenance_windows',
        blank=False,
        null=False
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        verbose_name='Virtual Machines',
        related_name='tasks_vm',
        blank = True
    )
    
    device = django_models.ManyToManyField(
        to='dcim.Device',
        verbose_name='Devices',
        related_name='tasks_device',
        blank = True
    )

    class Meta:
        verbose_name_plural = "Maintenance Tasks"
        verbose_name = 'Maintenance Task'
        ordering = ('name', 'maintenance_windows__start_time')

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenancetasks', args=[self.pk])
    
    def get_status_color(self):
        return TaskStatusChoices.colors.get(self.status)

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        from adestis_netbox_maintenance_management.plan_jobs import AutoCreateMaintenancePlannedActions
        AutoCreateMaintenancePlannedActions.enqueue(interval=JobIntervalChoices.INTERVAL_MINUTELY)
        return super().save(*args, **kwargs)
    
    def sync(self):
        from adestis_netbox_maintenance_management.plan_jobs import AutoCreateMaintenancePlannedActions
        AutoCreateMaintenancePlannedActions.enqueue()