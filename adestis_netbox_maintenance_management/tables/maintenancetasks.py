from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_maintenance_management.models import MaintenanceTasks, MaintenanceActions
from adestis_netbox_maintenance_management.filtersets import *
from dcim.models import *
from dcim.tables import *
from virtualization.models import *
from virtualization.forms import *
from virtualization.tables import *
import django_tables2 as tables
from netbox.tables.columns import ManyToManyColumn 
from netbox.tables.columns import BooleanColumn
from django.utils.safestring import mark_safe
from netbox.tables.columns import TemplateColumn
from django.utils.safestring import mark_safe
from django.db.models import Min, Max

class MaintenanceTasksTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    virtual_machine = columns.ManyToManyColumn(
        linkify = True,
        verbose_name="Virtual Machines",
        transform=lambda vm: vm.name,  # oder was du anzeigen willst
        orderable=False
    )
    
    def render_virtual_machine(self, value, record):
        # Hole alle VMs geordnet nach Name
        vms = value.all().order_by("name")

        # HTML für Checkboxen (untereinander mit Abstand)
        html_parts = []
        for vm in vms:
            checkbox_id = f"checkbox_{record.id}_{vm.id}"
            html_parts.append(f"""
                <div style="margin-bottom:8px;">
                    <label for="{checkbox_id}" style="margin-right:6px; pointer-events:none;">{vm.name}</label>
                    <input 
                        type="checkbox" 
                        id="{checkbox_id}" 
                        onclick="saveCheckboxState('{checkbox_id}')">
                </div>
            """)

        # JavaScript nur EINMAL anhängen
        # → prüft, ob Script schon existiert (damit es nur einmal eingefügt wird)
        js_script = """
        <script>
            if (!window.__vmCheckboxScriptLoaded) {
                document.addEventListener("DOMContentLoaded", function() {
                    document.querySelectorAll("input[id^='checkbox_']").forEach(cb => {
                        const saved = localStorage.getItem(cb.id);
                        if (saved === "true") cb.checked = true;
                    });
                });

                window.saveCheckboxState = function(id) {
                    const checkbox = document.getElementById(id);
                    localStorage.setItem(id, checkbox.checked);
                };

                window.__vmCheckboxScriptLoaded = true;
            }
        </script>
        """

        # HTML + Script zusammen zurückgeben
        return mark_safe("".join(html_parts) + js_script)
    
    device = columns.ManyToManyColumn(
        linkify_item = True,
        verbose_name= "Device"
    )
    
    maintenance_action = tables.Column(
        linkify= True
    )
    
    maintenance_windows = tables.Column(
        linkify= True
    )
    
        # 👉 Hier die neuen Felder aus dem verknüpften Modell:
    start_time = tables.TimeColumn(
        accessor="maintenance_windows.start_time",
        verbose_name="Start Time",
        format="H:i",
    )

    end_time = tables.TimeColumn(
        accessor="maintenance_windows.end_time",
        verbose_name="End Time",
        format="H:i" 
    )
    
    class Meta(NetBoxTable.Meta):

        model = MaintenanceTasks
        
        fields = ['virtual_machine', 'device', 'start_time', 'end_time', 'maintenance_action', 'maintenance_windows', 'name', 'description', 'tags', 'comments']
        default_columns = [ 'virtual_machine', 'device', 'name', 'start_time', 'end_time', 'maintenance_windows', 'maintenance_action', 'comments']

    # Sortierbar machen
    def order_start_time(self, queryset, is_descending):
        queryset = queryset.annotate(min_start=Min('maintenance_windows__start_time'))
        order_field = '-min_start' if is_descending else 'min_start'
        return queryset.order_by(order_field), True

    def order_end_time(self, queryset, is_descending):
        queryset = queryset.annotate(max_end=Max('maintenance_windows__end_time'))
        order_field = '-max_end' if is_descending else 'max_end'
        return queryset.order_by(order_field), True



        