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
        verbose_name='Refrence Number',
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

    class Meta:
        verbose_name_plural = "Maintenance Plans"
        verbose_name = 'Maintenance Plan'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenanceplans', args=[self.pk])

    def __str__(self):
        return self.name 