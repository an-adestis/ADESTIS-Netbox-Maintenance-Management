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

class MaintenanceTasksTable(NetBoxTable):
    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()
    
    name = columns.MarkdownColumn(
        linkify=True
    )

    description = columns.MarkdownColumn()
    
    virtual_machine = tables.ManyToManyColumn(
        linkify=True,
        verbose_name="Virtual Machines",
        transform=lambda vm: vm.name,  # oder was du anzeigen willst
        orderable=False
    )
    
    device = columns.ManyToManyColumn(
        linkify = True,
        verbose_name= "Device"
    )
    
    maintenance_action = tables.Column(
        linkify= True
    )
    
    maintenance_windows = tables.Column(
        linkify= True
    )
    
    done = columns.TemplateColumn(
        template_code="""
            <input type="checkbox" id="checkbox_{{ record.id }}" onclick="CookiesCheck({{ record.id }})">
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    var checkbox = document.getElementById("checkbox_{{ record.id }}");
                    if (localStorage.getItem("checkbox_{{ record.id }}") === "true") {
                        checkbox.checked = true;
                    }
                });

                function CookiesCheck(id) {
                    var checkbox = document.getElementById("checkbox_" + id);
                    localStorage.setItem("checkbox_" + id, checkbox.checked);
                }
            </script>
        """,
        verbose_name="Done",
        orderable=False
    )
    
    from django.utils.safestring import mark_safe

    def render_virtual_machine(self, value, record):
        vms = value.all().order_by("name")

        # HTML: jede VM + Checkbox + Abstand
        html_parts = []
        for vm in vms:
            html_parts.append(f"""
                <div style="margin-bottom:10px;">
                    <input type="checkbox" id="checkbox_{record.id}_{vm.id}" onclick="CookiesCheck({record.id}, {vm.id})">
                    <label for="checkbox_{record.id}_{vm.id}">{vm}</label>
                </div>
            """)

        # JS: DOMContentLoaded + CookiesCheck
        js = """
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                document.querySelectorAll("input[id^='checkbox_']").forEach(cb => {
                    if (localStorage.getItem(cb.id) === "true") {
                        cb.checked = true;
                    }
                });
            });

            function CookiesCheck(recordId, vmId) {
                var id = 'checkbox_' + recordId + '_' + vmId;
                var checkbox = document.getElementById(id);
                localStorage.setItem(id, checkbox.checked);
            }
        </script>
        """

        return mark_safe("".join(html_parts) + js)

    class Meta(NetBoxTable.Meta):

        model = MaintenanceTasks
        
        fields = ['virtual_machine', 'device', 'maintenance_action', 'maintenance_windows', 'name', 'description', 'tags', 'comments', 'done']
        default_columns = [ 'name', 'maintenance_windows', 'maintenance_action', 'virtual_machine', 'device', 'done', 'comments']


        