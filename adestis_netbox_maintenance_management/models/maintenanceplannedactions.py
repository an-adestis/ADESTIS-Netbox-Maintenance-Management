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
from adestis_netbox_maintenance_management.models import *
from core.choices import JobIntervalChoices

__all__ = (
    'MaintenancePlannedActions',
)

class MaintenancePlannedActions(NetBoxModel):

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
    
    maintenance_action = django_models.ManyToManyField(
        to='adestis_netbox_maintenance_management.MaintenanceActions',
        blank=False,
        related_name='plans_maintenance_actions',
        verbose_name='Maintenance Actions',
    )
    
    maintenance_windows = django_models.ManyToManyField(
        to='adestis_netbox_maintenance_management.MaintenanceWindows',
        blank=False,
        related_name='plans_maintenance_windows',
        verbose_name='Maintenance Windows',
    )
    
    maintenance_tasks = django_models.ManyToManyField(
        to='adestis_netbox_maintenance_management.MaintenanceTasks',
        verbose_name='Maintenance Tasks',
        related_name='plans_tasks',
        blank = True
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        verbose_name='Virtual Machines',
        related_name='plans_vm',
        blank = True
    )
    
    device = django_models.ManyToManyField(
        to='dcim.Device',
        verbose_name='Devices',
        related_name='plans_device',
        blank = True
    )
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'maintenance_tenant',
         null = True,
         verbose_name='Tenant',
         blank = True
     )
    
    tasks = django_models.ManyToManyField(
        to='MaintenanceTasks',
        blank=True,
        related_name='plans'
    )
    
    grouping_key = django_models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "Planned Actions"
        verbose_name = 'Planned Action'
        ordering = ('name',)

    # def get_absolute_url(self):
    #     return reverse('plugins:adestis_netbox_maintenance_management:maintenanceplannedactions', args=[self.pk])

    def __str__(self):
        return self.name 