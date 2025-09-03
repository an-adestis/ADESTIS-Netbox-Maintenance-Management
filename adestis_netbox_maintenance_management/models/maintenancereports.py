from datetime import date, timedelta
from adestis_netbox_maintenance_management.models import MaintenancePlans, MaintenanceActions

def get_kunden_report_data(tenant_id):
    plans = MaintenancePlans.objects.filter(
        tenant_id=tenant_id
    ).select_related(
        'maintenance_action',
        'maintenance_action__maintenance_window',
        'tenant'
    ).prefetch_related(
        'maintenance_action__device',
        'maintenance_action__virtual_machine'
    )
    return {
        'plans': plans
    }

def get_adestis_report_data():
    today = date.today()
    end = today + timedelta(days=7)

    actions = MaintenanceActions.objects.filter(
        maintenance_window__start_time__lte=end,
        maintenance_window__end_time__gte=today
    ).prefetch_related(
        'device',
        'virtual_machine',
        'maintenance_window'
    )

    return {
        'actions': actions,
        'today': today,
        'end': end,
    }
