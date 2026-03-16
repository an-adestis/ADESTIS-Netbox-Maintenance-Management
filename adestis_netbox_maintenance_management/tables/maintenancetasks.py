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
    
    status = ChoiceFieldColumn()

    description = columns.MarkdownColumn()
    
    virtual_machine = columns.ManyToManyColumn(
        linkify = True,
        verbose_name="Virtual Machines",
        transform=lambda vm: vm.name,  
        orderable=False
    )
    
    def render_virtual_machine(self, value, record):
        vms = value.all()
        
        html_parts = ['<ul style="list-style:none; padding-left:2px; width:500px;">']

        for i, vm in enumerate(vms):

            checkbox_id = f"checkbox_{record.id}_{vm.id}"
            checkbox_html = f'<input type="checkbox" id="{checkbox_id}" onclick="saveCheckboxState(\'{checkbox_id}\')">'

            vm_link = f'<a href="{vm.get_absolute_url()}" style="margin-right:6px;">{vm.name}</a>'
            

            html_parts.append(f'''
            <li style="padding:6px 0; border-bottom:1px solid #ccc;">
                <div style="
                    display:inline-block; 
                    width:500px;           /* maximale Breite der VM-Spalte */
                    white-space:normal;    /* Zeilenumbruch erlauben */
                    word-break:break-word; /* sehr lange Worte umbrechen */
                    vertical-align:top;
                ">
                    {checkbox_html} {vm_link}
                    <br>
                    <small style="color:#ccc;">{getattr(vm, "comments", "-")}</small>
                </div>
            </li>
            ''')

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

        return mark_safe("".join(html_parts) + js_script)
    
    device = columns.ManyToManyColumn(
        linkify_item = True,
        verbose_name= "Device"
    )
    
    def render_device(self, value, record):
        devices = value.all()
        
        html_parts = ['<ul style="list-style:none; padding-left:2px; width:500px;">']

        for i, device in enumerate(devices):
            
            device_link = f'<a href="{device.get_absolute_url()}" style="margin-right:6px;">{device.name}</a>'
            

            html_parts.append(f'''
            <li style="padding:6px 0; border-bottom:1px solid #ccc;">
                <div style="
                    display:inline-block; 
                    width:200px;           /* maximale Breite der VM-Spalte */
                    white-space:normal;    /* Zeilenumbruch erlauben */
                    word-break:break-word; /* sehr lange Worte umbrechen */
                    vertical-align:top;
                ">
                     {device_link}
                    <br>
                    <small style="color:#ccc;">{getattr(device, "comments", "-")}</small>
                </div>
            ''')

        return mark_safe("".join(html_parts))
        
    maintenance_action = tables.Column(
        linkify= True
    )
    #wegen der länge schauen
    def render_maintenance_action(self, value, record):
        if not value:
            return "-"

        maintenanceaction = value

        maintenanceaction_link = (
            f'<a href="{maintenanceaction.get_absolute_url()}" '
            f'style="margin-right:6px;">{maintenanceaction.name}</a>'
        )

        html = f'''
        <div style="width:300px; word-break:break-word;">
            {maintenanceaction_link}
            <br>
            <small style="color:#ccc;">
                {getattr(maintenanceaction, "comments", "-")}
            </small>
        </div>
        '''

        return mark_safe(html)

    
    maintenance_windows = tables.Column(
        linkify= True
    )

    start_time = tables.TimeColumn(
        accessor="maintenance_windows.start_time",
        verbose_name="Start Time (Local Time)",
        format="H:i",
        order_by = ('start_time',)
    )

    end_time = tables.TimeColumn(
        accessor="maintenance_windows.end_time",
        verbose_name="End Time (Local Time)",
        format="H:i",
    )
    
    class Meta(NetBoxTable.Meta):

        model = MaintenanceTasks
        
        fields = ['virtual_machine', 'device', 'status', 'start_time', 'end_time', 'maintenance_action', 'maintenance_windows', 'name', 'description', 'tags', 'comments', 'next_due_date']
        default_columns = ['maintenance_action', 'virtual_machine', 'device', 'name', 'status', 'start_time', 'end_time', 'maintenance_windows', 'next_due_date']        