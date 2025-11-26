from .maintenancewindows import *
from .maintenanceactions import *
from .maintenanceplannedactions import *
from .maintenancereports import *
from .maintenancetasks import *
from .maintenanceplans import *
from datetime import datetime, date, timedelta

from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.shortcuts import redirect, render
from adestis_netbox_maintenance_management.models import MaintenanceTasks, MaintenancePlannedActions
from io import BytesIO

def generate_pdf(request, pk):
    today = date.today()
    return FileResponse(
        generate_pdf_file(request, pk), 
        as_attachment=True,
        filename=f"{today}_maintenance_plan_{pk}.pdf"
    )

def generate_pdf_file(request, pk):
    plan = MaintenancePlannedActions.objects.get(pk=pk)
    # Filter: Nur Tasks zu diesem Plan
    maintenance_tasks = plan.maintenance_tasks.all()

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    y = 750
    for task in maintenance_tasks:
        window = task.maintenance_windows.name if task.maintenance_windows else "-"
        action = task.maintenance_action.name if task.maintenance_action else "-"
        vms = ", ".join([str(vm) for vm in task.virtual_machine.all()])
        devices = ", ".join([str(d) for d in task.device.all()])

        p.drawString(100, y, f"Window: {window}")
        p.drawString(100, y - 15, f"Action: {action}")
        p.drawString(100, y - 30, f"VMs: {vms if vms else '-'}")
        p.drawString(100, y - 45, f"Devices: {devices if devices else '-'}")

        y -= 80
        if y < 50:
            p.showPage()
            y = 750

    p.save()
    buffer.seek(0)
    return buffer

# Report engine auf html ebene arbeiten statt mit canvas 
# html jinja2 html report pdf 
