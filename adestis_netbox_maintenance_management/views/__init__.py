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

class MaintenancePlansPDF(FPDF, HTMLMixin):

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Maintenance Plan by Time", 0, 1, "L")

        self.set_font("Helvetica", "", 11)
        self.cell(0, 8, datetime.today().strftime('%d.%m.%Y'), 0, 1, "C")
        self.ln(5)


def get_line_count(pdf, text, col_width):
    # Alles in String umwandeln – None, int, bool etc. safe
    text = "" if text is None else str(text)

    # Lines berechnen – wir splitten einfach an Leerzeichen
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
    
from django.http import HttpResponse
from django.views import View

class MaintenancePlanPDFView(View):

    def get(self, request):
        plans = MaintenancePlans.objects.all()

        pdf = MaintenancePlansPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)

        headers = ["Ref Number", "Done", "Name", "Description", "Tenant"]
        col_widths = [30, 12, 45, 73, 30]
        LINE_HEIGHT = 5

        # Tabellenkopf
        pdf.set_font("Helvetica", "B", 10)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 8, header, border=1, align="C")
        pdf.ln()
        pdf.set_font("Helvetica", "", 10)

        # ---------------------------------------------
        # ÜBER ALLE PLÄNE ITERIEREN
        # ---------------------------------------------
        for plan in plans:

            ref_number = plan.refrence_number or ""
            done = "X"
            name = plan.name or ""
            description = plan.description or ""
            tenant = str(plan.tenant) if plan.tenant else ""

            line_counts = [
                get_line_count(pdf, ref_number, col_widths[0]),
                get_line_count(pdf, done, col_widths[1]),
                get_line_count(pdf, name, col_widths[2]),
                get_line_count(pdf, description, col_widths[3]),
                get_line_count(pdf, tenant, col_widths[4]),
            ]

            row_height = max(line_counts) * LINE_HEIGHT
            x_start = pdf.get_x()
            y_start = pdf.get_y()

            # Rahmen
            x = x_start
            for width in col_widths:
                pdf.rect(x, y_start, width, row_height)
                x += width

            # Inhalte
            pdf.multi_cell(col_widths[0], LINE_HEIGHT, str(ref_number), align="C")
            pdf.set_xy(x_start + col_widths[0], y_start)

            pdf.multi_cell(col_widths[1], LINE_HEIGHT, str(done), align="C")
            pdf.set_xy(x_start + col_widths[0] + col_widths[1], y_start)

            pdf.multi_cell(col_widths[2], LINE_HEIGHT, str(name), align="C")
            pdf.set_xy(
                x_start + col_widths[0] + col_widths[1] + col_widths[2],
                y_start
            )

            pdf.multi_cell(col_widths[3], LINE_HEIGHT, str(description))
            pdf.set_xy(
                x_start
                + col_widths[0]
                + col_widths[1]
                + col_widths[2]
                + col_widths[3],
                y_start
            )

            pdf.multi_cell(col_widths[4], LINE_HEIGHT, str(tenant))

            pdf.set_xy(x_start, y_start + row_height)

        response = HttpResponse(
            pdf.output(dest="S").encode("latin-1"),
            content_type="application/pdf"
        )
        
        response["Content-Disposition"] = f'attachment; filename="maintenance_plans_{datetime.today()}.pdf"'
        return response

class MaintenanceActionPlanPDFView(View):

    LINE_HEIGHT = 5

    def render_m2m_cell(self, pdf, x, y, width, relation):
        pdf.set_xy(x, y)

        if relation is None:
            return

        # ManyToMany / QuerySet
        if hasattr(relation, "all"):
            for obj in relation.all():
                pdf.multi_cell(width, self.LINE_HEIGHT, str(obj), border=0, align='C')
                y += self.LINE_HEIGHT * self.get_num_lines(pdf, str(obj), width)
                pdf.set_xy(x, y)
            return

        # ForeignKey / einzelnes Objekt
        pdf.multi_cell(width, self.LINE_HEIGHT, str(relation), border=0, align='C')

    def get_relation_text(self, relation):
        if relation is None:
            return ""

        if hasattr(relation, "all"):
            return "\n".join([str(obj) for obj in relation.all()])

        return str(relation)

    def get_num_lines(self, pdf, text, width):
        if not text:
            return 1

        words = str(text).split(' ')
        line = ""
        lines = 1

        for word in words:
            if pdf.get_string_width(line + " " + word) <= width:
                line += " " + word
            else:
                lines += 1
                line = word

        return lines

    def get(self, request, pk):

        actions = MaintenanceTasks.objects.all()

        pdf = MaintenancePlansPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)

        col_widths = [40, 40, 40, 40, 30]

        for action in actions:
            description = action.description or ""

            x_start = pdf.get_x()
            y_start = pdf.get_y()

            # === Dynamische Zeilenhöhe berechnen ===
            lines = []

            # Maintenance Windows
            mw_text = self.get_relation_text(action.maintenance_windows)
            lines.append(self.get_num_lines(pdf, mw_text, col_widths[0]))

            # Maintenance Actions
            ma_text = self.get_relation_text(action.maintenance_action)
            lines.append(self.get_num_lines(pdf, ma_text, col_widths[1]))

            # Virtual Machines
            vm_text = self.get_relation_text(action.virtual_machine)
            lines.append(self.get_num_lines(pdf, vm_text, col_widths[2]))

            # Description
            lines.append(self.get_num_lines(pdf, description, col_widths[3]))

            # Devices
            dev_text = self.get_relation_text(action.device)
            lines.append(self.get_num_lines(pdf, dev_text, col_widths[4]))

            row_height = max(lines) * self.LINE_HEIGHT

            # === Rahmen zeichnen ===
            x = x_start
            for width in col_widths:
                pdf.rect(x, y_start, width, row_height)
                x += width

            # === Inhalte ===
            self.render_m2m_cell(pdf, x_start, y_start, col_widths[0], action.maintenance_windows)
            self.render_m2m_cell(pdf, x_start + col_widths[0], y_start, col_widths[1], action.maintenance_action)
            self.render_m2m_cell(pdf, x_start + col_widths[0] + col_widths[1], y_start, col_widths[2], action.virtual_machine)

            pdf.set_xy(x_start + col_widths[0] + col_widths[1] + col_widths[2], y_start)
            pdf.multi_cell(col_widths[3], self.LINE_HEIGHT, description)

            self.render_m2m_cell(
                pdf,
                x_start + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3],
                y_start,
                col_widths[4],
                action.device
            )

            pdf.set_xy(x_start, y_start + row_height)

        response = HttpResponse(
            pdf.output(dest="S").encode("latin-1"),
            content_type="application/pdf",
        )
        response["Content-Disposition"] = f'attachment; filename="planned_actions_{datetime.today()}.pdf"'
        return response


