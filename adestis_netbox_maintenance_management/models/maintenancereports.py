from datetime import date, timedelta
from adestis_netbox_maintenance_management.models import MaintenancePlannedActions, MaintenanceActions
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


class MaintenanceReport(NetBoxModel):
    
    maintenance_planned_actions = django_models.ForeignKey(
        to='adestis_netbox_maintenance_management.MaintenancePlannedActions',
        on_delete= django_models.PROTECT,
        related_name='maintenance_planned_actions',
        blank=False,
        null=False
    )
    
    name = django_models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name_plural = "Maintenance Reports"
        verbose_name = 'Maintenance Report'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenancereports', args=[self.pk])

    def __str__(self):
        return self.name 