from rest_framework import serializers
from adestis_netbox_maintenance_management.models import *
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.models import *
from tenancy.api.serializers import *
from dcim.api.serializers import *
from dcim.models import *
from virtualization.api.serializers import *

class MaintenancePlannedActionsSerializer(NetBoxModelSerializer):

    class Meta:
        model = MaintenancePlannedActions
        fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                  'custom_field_data', 'description', 'maintenance_action', 'tenant')
        brief_fields = ('id', 'tags', 'custom_fields', 'display', 'created', 'last_updated',
                        'custom_field_data', 'description', 'maintenance_action', 'tenant')

