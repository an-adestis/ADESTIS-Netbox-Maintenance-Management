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
        def header(self):
            # Titel
            self.set_font("Helvetica", "B", 14)
            self.cell(0, 10, "Maintenance Plan by Time", 0, 0, "L")
            # Optionales Logo
            # self.image('static/images/adestis_logo.png', x=170, y=8, w=30)
            self.ln(15)
            # KW und Datum zentriert
            self.set_font("Helvetica", "B", 12)
            from datetime import datetime
            today = datetime.today()
            self.cell(0, 10, f"KW {today.isocalendar()[1]}, {today.strftime('%d.%m.%Y')}", 0, 1, "C")
            self.ln(5)

def export_pdf(request, pk):
    plan = MaintenancePlans.objects.get(pk=pk)
    entries = plan.entries.all().order_by('sched_start')  # alle Termine des Plans

    pdf = MaintenancePlansPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=10)

    # Tabelle: Spalten und Breiten
    headers = ["Scheduled Start", "Scheduled End", "Done?", "Details", "Name", "Management URL", "ActionName", "Site"]
    col_widths = [25, 25, 15, 30, 40, 40, 30, 25]

    # Tabellenkopf
    pdf.set_font("Helvetica", "B", 10)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)

    for entry in entries:
        # dynamische Werte holen
        start = entry.sched_start.strftime("%H:%M") if entry.sched_start else ""
        end = entry.sched_end.strftime("%H:%M") if entry.sched_end else ""
        done = "✓" if entry.is_done else ""
        details = entry.details or ""
        name = entry.name or ""
        management_url = entry.management_url or ""
        action_name = entry.action_name or ""
        site = entry.site or ""

        # Maximum Zeilenhöhe für MultiCell (falls Name oder Details lang sind)
        lines_name = max(name.count('\n') + 1, 1)
        lines_details = max(details.count('\n') + 1, 1)
        max_lines = max(lines_name, lines_details, 1)

        pdf.cell(col_widths[0], 8*max_lines, start, border=1)
        pdf.cell(col_widths[1], 8*max_lines, end, border=1)
        pdf.cell(col_widths[2], 8*max_lines, done, border=1, align="C")

        # Details
        x_before = pdf.get_x()
        y_before = pdf.get_y()
        pdf.multi_cell(col_widths[3], 8, details, border=1)
        pdf.set_xy(x_before + col_widths[3], y_before)

        # Name
        x_before = pdf.get_x()
        y_before = pdf.get_y()
        pdf.multi_cell(col_widths[4], 8, name, border=1)
        pdf.set_xy(x_before + col_widths[4], y_before)

        # Management URL
        x_before = pdf.get_x()
        y_before = pdf.get_y()
        pdf.multi_cell(col_widths[5], 8, management_url, border=1)
        pdf.set_xy(x_before + col_widths[5], y_before)

        # ActionName
        x_before = pdf.get_x()
        y_before = pdf.get_y()
        pdf.multi_cell(col_widths[6], 8, action_name, border=1)
        pdf.set_xy(x_before + col_widths[6], y_before)

        # Site
        pdf.cell(col_widths[7], 8*max_lines, site, border=1)
        pdf.ln()

    # PDF als Response
    response = HttpResponse(
        pdf.output(dest="S").encode("latin-1", errors="replace"),  # Haken ✓ wird ersetzt, sonst UTF-8 nötig
        content_type="application/pdf",
    )
    response["Content-Disposition"] = f'attachment; filename="maintenance_plan_{plan.pk}.pdf"'
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