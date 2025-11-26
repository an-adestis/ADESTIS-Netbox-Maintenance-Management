from rest_framework import serializers
from adestis_netbox_maintenance_management.models import *
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *

class MaintenanceReportSerializer(NetBoxModelSerializer):

    class Meta:
        model = MaintenanceReport
        fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                  'custom_field_data', 'maintenance_planned_actions')
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                        'custom_field_data', 'maintenance_planned_actions')

