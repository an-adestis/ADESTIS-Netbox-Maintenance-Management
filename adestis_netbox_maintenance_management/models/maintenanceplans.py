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

__all__ = (
    'MaintenancePlans',
)

class MaintenancePlans(NetBoxModel):
    
    name = django_models.CharField(
        max_length=150
    )
    
    reference_number = django_models.IntegerField(
        verbose_name='Reference Number',
        blank=True,
        null = True
    )
    
    description = django_models.CharField(
        max_length=500,
        blank = True
    )
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'plans_tenant',
         null = True,
         verbose_name='Tenant',
         blank = True
    )
    
    maintenance_windows = django_models.ManyToManyField(
        to='adestis_netbox_maintenance_management.MaintenanceWindows',
        blank=False,
        related_name='maintenance_windows_plans',
        verbose_name='Maintenance Windows',
    )
    
    maintenance_action = django_models.ManyToManyField(
        to='adestis_netbox_maintenance_management.MaintenanceActions',
        verbose_name='Maintenance Actions',
        related_name='maintenance_action_plans',
        blank=False,
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        verbose_name='Virtual Machines',
        related_name='vm_plans',
        blank = True
    )
    
    device = django_models.ManyToManyField(
        to='dcim.Device',
        verbose_name='Devices',
        related_name='device_plans',
        blank = True
    )
    
    version = django_models.CharField(
        blank = True, 
        null = True
    )

    class Meta:
        verbose_name_plural = "Maintenance Plans"
        verbose_name = 'Maintenance Plan'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenanceplans', args=[self.pk])

    def __str__(self):
        return self.name 
    
    # bei maintenance plans action mit rein nehmen inklsuive tab, version feld, auch alles anzeigen wie vm's und co 
    