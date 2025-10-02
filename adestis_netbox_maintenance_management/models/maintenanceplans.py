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

__all__ = (
    'MaintenancePlans',
)

class MaintenancePlans(NetBoxModel):

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
        null=False
    )
    
    tenant = django_models.ForeignKey(
         to = 'tenancy.Tenant',
         on_delete = django_models.PROTECT,
         related_name = 'maintenance_tenant',
         null = True,
         verbose_name='Tenant',
         blank = True
     )

    class Meta:
        verbose_name_plural = "Maintenance Plans"
        verbose_name = 'Maintenance Plans'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenanceplans', args=[self.pk])

    def __str__(self):
        return self.name 
    
    # def save(self, *args, **kwargs):
    #     from adestis_netbox_maintenance_management.jobs import AutoCreateMaintenancePlans
    #     AutoCreateMaintenancePlans.enqueue_once(instance=self, interval=JobIntervalChoices.INTERVAL_HOURLY)
    #     return super().save(*args, **kwargs)

    # def sync(self):
    #     from adestis_netbox_maintenance_management.jobs import AutoCreateMaintenancePlans
    #     AutoCreateMaintenancePlans.enqueue()
    
    
