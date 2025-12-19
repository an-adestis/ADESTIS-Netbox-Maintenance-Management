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
from adestis_netbox_maintenance_management.models import MaintenancePlans, MaintenancePlannedActions, MaintenanceTasks
from io import BytesIO
from django.http import HttpResponse
from fpdf import FPDF, HTMLMixin

class MaintenancePlansPDF(FPDF, HTMLMixin):
    pass

def export_pdf(request, pk):
    plan = MaintenancePlans.objects.get(pk=pk)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", size=12)

    pdf.multi_cell(0, 10, f"Maintenance Plan: {plan.name}")
    pdf.ln(3)
    
    pdf.multi_cell(0, 10, f"Tenant: {plan.tenant}")

    pdf.multi_cell(0, 8, f"Reference: {plan.refrence_number}")
    pdf.ln(3)

    pdf.multi_cell(0, 8, f"Description:\n{plan.description or ''}")

    response = HttpResponse(
        pdf.output(dest="S").encode("latin-1"),
        content_type="application/pdf",
    )
    response["Content-Disposition"] = (
        f'attachment; filename="maintenance_plan_{plan.name}.pdf"'
    )

    return response

def export_planned_action_pdf(request, pk):
    # Objekt holen
    action = MaintenancePlannedActions.objects.get(pk=pk)
    tasks_window = MaintenanceTasks

    # Neues PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    # Header
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Planned Action: {action.name}", ln=True)
    pdf.ln(5)

    # Description
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Description:", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 6, action.description or "-")
    pdf.ln(3)

    # Maintenance Actions (ManyToMany)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Maintenance Actions:", ln=True)
    pdf.set_font("Helvetica", size=12)
    actions_list = "\n".join(str(a) for a in action.maintenance_action.all())
    pdf.multi_cell(0, 6, actions_list or "-")

    pdf.ln(3)

    # Maintenance Windows (ManyToMany)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Maintenance Windows:", ln=True)
    pdf.set_font("Helvetica", size=12)
    windows_list = "\n".join(str(w) for w in action.maintenance_windows.all())
    pdf.multi_cell(0, 6, windows_list or "-")
    pdf.ln(3)

    # Maintenance Tasks (ManyToMany)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Maintenance Tasks:", ln=True)
    tasks_list = "\n".join(str(t) for t in action.maintenance_tasks.all())
    pdf.multi_cell(0, 6, tasks_list or "-")
    pdf.ln(3)

    # Virtual Machines (ManyToMany)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Virtual Machines:", ln=True)
    pdf.set_font("Helvetica", size=12)
    vm_list = "\n".join(str(vm) for vm in action.virtual_machine.all())
    pdf.multi_cell(0, 6, vm_list or "-")
    pdf.ln(3)

    # Devices (ManyToMany)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Devices:", ln=True)
    pdf.set_font("Helvetica", size=12)
    devices_list = "\n".join(str(dev) for dev in action.device.all())
    pdf.multi_cell(0, 6, devices_list or "-")
    pdf.ln(3)

    # Comments
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Comments:", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 6, action.comments or "-")
    pdf.ln(3)

    # PDF zurückgeben
    response = HttpResponse(
        pdf.output(dest="S").encode("latin-1"),
        content_type="application/pdf",
    )
    response["Content-Disposition"] = f'attachment; filename="planned_action_{action.pk}.pdf"'

    return response