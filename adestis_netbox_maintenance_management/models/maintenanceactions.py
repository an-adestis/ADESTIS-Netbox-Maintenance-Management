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
    
    def __str__(self):
        return f"{self.get_recurrence_type_display()}"

    class Meta:
        verbose_name_plural = "Maintenance Actions"
        verbose_name = 'Maintenance Action'

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenanceactions', args=[self.pk])

    def __str__(self):
        return self.name 
    
    
