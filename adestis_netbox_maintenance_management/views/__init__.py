from .maintenancewindows import *
from .maintenanceactions import *
from .maintenanceplannedactions import *
from .maintenancereports import *
from .maintenancetasks import *
from .maintenanceplans import *
from datetime import datetime, date, timedelta

from django.http import FileResponse
from reportlab.pdfgen import canvas
from netbox.views import generic

from django.shortcuts import redirect, render
from adestis_netbox_maintenance_management.models import MaintenancePlans, MaintenancePlannedActions, MaintenanceTasks
from io import BytesIO
from django.http import HttpResponse
from fpdf import FPDF, HTMLMixin

class MaintenancePlansPDF(FPDF, HTMLMixin, generic.ObjectListView):
    queryset = MaintenancePlans.objects.all()
    template_name = "adestis_netbox_maintenance_management/maintenance_plans.html"

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Maintenance Plan by Time", 0, 1, "L")

        self.set_font("Helvetica", "", 11)
        self.cell(0, 8, datetime.today().strftime('%d.%m.%Y'), 0, 1, "C")
        self.ln(5)


# =====================================================
# Hilfsfunktion: echte Zeilenanzahl berechnen
# =====================================================
def get_line_count(pdf, text, col_width):
    if not text:
        return 1

    text = str(text).replace("\r", "")
    words = text.split(" ")
    lines = 1
    line_width = 0

    for word in words:
        word_width = pdf.get_string_width(word + " ")
        if line_width + word_width <= col_width:
            line_width += word_width
        else:
            lines += 1
            line_width = word_width

    return lines


# =====================================================
# PDF Export View
# =====================================================
def export_pdf(request, pk):

    plan = MaintenancePlans.objects.get(pk=pk)

    pdf = MaintenancePlansPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)

    # -------------------------------------------------
    # Tabellen-Definition
    # -------------------------------------------------
    headers = ["Ref Number", "Done", "Name", "Description", "Tenant"]
    col_widths = [30, 12, 45, 73, 30]  # Summe = 190 (A4)

    LINE_HEIGHT = 5

    # -------------------------------------------------
    # Tabellenkopf
    # -------------------------------------------------
    pdf.set_font("Helvetica", "B", 10)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)

    # -------------------------------------------------
    # Daten
    # -------------------------------------------------
    ref_number = plan.refrence_number or ""
    done = "X"
    name = plan.name or ""
    description = plan.description or ""
    tenant = str(plan.tenant) if plan.tenant else ""

    # -------------------------------------------------
    # Dynamische Zeilenhöhe bestimmen
    # -------------------------------------------------
    line_counts = [
        get_line_count(pdf, ref_number, col_widths[0]),
        get_line_count(pdf, done, col_widths[1]),
        get_line_count(pdf, name, col_widths[2]),
        get_line_count(pdf, description, col_widths[3]),
        get_line_count(pdf, tenant, col_widths[4]),
    ]

    max_lines = max(line_counts)
    row_height = max_lines * LINE_HEIGHT

    x_start = pdf.get_x()
    y_start = pdf.get_y()

    # -------------------------------------------------
    # Rahmen für komplette Tabellenzeile
    # -------------------------------------------------
    x = x_start
    for width in col_widths:
        pdf.rect(x, y_start, width, row_height)
        x += width

    # -------------------------------------------------
    # Zellinhalte (ohne Border!)
    # -------------------------------------------------
    pdf.multi_cell(col_widths[0], LINE_HEIGHT, str(ref_number), align="C")
    pdf.set_xy(x_start + col_widths[0], y_start)

    pdf.multi_cell(col_widths[1], LINE_HEIGHT, done, align="C")
    pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)

    pdf.multi_cell(col_widths[2], LINE_HEIGHT, name, align="C")
    pdf.set_xy(
        x_start + col_widths[0] + col_widths[1] + col_widths[2],
        y_start
    )

    pdf.multi_cell(col_widths[3], LINE_HEIGHT, description)
    pdf.set_xy(
        x_start
        + col_widths[0]
        + col_widths[1]
        + col_widths[2]
        + col_widths[3],
        y_start
    )

    pdf.multi_cell(col_widths[4], LINE_HEIGHT, tenant, align="C")

    # Cursor unter die Zeile setzen
    pdf.set_xy(x_start, y_start + row_height)

    # -------------------------------------------------
    # HTTP Response → DOWNLOAD erzwingen
    # -------------------------------------------------
    response = HttpResponse(
        pdf.output(dest="S").encode("latin-1"),
        content_type="application/pdf"
    )
    response["Content-Disposition"] = (
        'attachment; filename="maintenance_plan.pdf"'
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