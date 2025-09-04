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
from adestis_netbox_maintenance_management.models import MaintenanceWindows


__all__ = (
    'MaintenanceActions',
)

class MaintenanceActions(NetBoxModel):

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
    
    maintenance_window = django_models.ForeignKey(
        to='adestis_netbox_maintenance_management.MaintenanceWindows',
        on_delete= django_models.PROTECT,
        related_name='maintenance_window',
        blank=False,
        null=False
    )
    
    device = django_models.ManyToManyField(
        to='dcim.Device',
        verbose_name='Devices',
        related_name='maintenance_actions',
        blank = True
    )
    
    virtual_machine = django_models.ManyToManyField(
        to='virtualization.VirtualMachine',
        verbose_name='Virtual Machines',
        related_name='maintenance_actions',
        blank = True
    )
    

    class Meta:
        verbose_name_plural = "Maintenance Actions"
        verbose_name = 'Maintenance Action'

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions', args=[self.pk])

    def __str__(self):
        return self.name 
    
    
