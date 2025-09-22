from datetime import date, timedelta
from adestis_netbox_maintenance_management.models import MaintenancePlans, MaintenanceActions
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
    
    maintenance_plans = django_models.ForeignKey(
        to='adestis_netbox_maintenance_management.MaintenancePlans',
        on_delete= django_models.PROTECT,
        related_name='maintenance_plans',
        blank=False,
        null=False
    )
    
    name = django_models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

# def get_kunden_report_data(tenant_id):
#     plans = MaintenancePlans.objects.filter(
#         tenant_id=tenant_id
#     ).select_related(
#         'maintenance_action',
#         'maintenance_action__maintenance_window',
#         'tenant'
#     ).prefetch_related(
#         'maintenance_action__device',
#         'maintenance_action__virtual_machine'
#     )
#     return {
#         'plans': plans
#     }

# def get_adestis_report_data():
#     today = date.today()
#     end = today + timedelta(days=7)

#     actions = MaintenanceActions.objects.filter(
#         maintenance_window__start_time__lte=end,
#         maintenance_window__end_time__gte=today
#     ).prefetch_related(
#         'device',
#         'virtual_machine',
#         'maintenance_window'
#     )

#     return {
#         'actions': actions,
#         'today': today,
#         'end': end,
#     }

    class Meta:
        verbose_name_plural = "Maintenance Reports"
        verbose_name = 'Maintenance Report'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_maintenance_management:maintenancereports', args=[self.pk])

    def __str__(self):
        return self.name 