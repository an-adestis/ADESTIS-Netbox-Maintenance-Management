from .maintenancewindows import *
from .maintenanceactions import *
from .maintenanceplannedactions import *
from .pdf import *
from .maintenancetasks import *
from .maintenanceplans import *
from datetime import datetime, date, timedelta

from django.http import FileResponse
from reportlab.pdfgen import canvas
from netbox.views import generic

from django.shortcuts import redirect, render
from adestis_netbox_maintenance_management.models import MaintenancePlans, MaintenancePlannedActions, MaintenanceTasks, MaintenanceActions
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

    text = "" if text is None else str(text)

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
from django.contrib import messages

class MaintenancePlanPDFView(View):
    
    def post(self, request):
        # POST soll sich wie GET verhalten,
        # aber mit ausgewählten IDs

        selected_ids = request.POST.getlist("pk")

        # Trick: wir speichern die IDs am Request,
        # damit get() sie benutzen kann
        request.selected_ids = selected_ids

        return self.get(request)

    def get(self, request, **kwargs):
        
        selected_ids = request.POST.getlist("pk")

        if not selected_ids:
            messages.warning(request, "No Maintenance Plans were selected.")
            return redirect(request.META.get("HTTP_REFERER"))

        plans = MaintenancePlans.objects.filter(pk__in=selected_ids)

        pdf = MaintenancePlansPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)

        headers = ["Ref Number", "Done", "Name", "Description", "Tenant"]
        col_widths = [30, 12, 45, 73, 30]
        LINE_HEIGHT = 5

        pdf.set_font("Helvetica", "B", 10)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 8, header, border=1, align="C")
        pdf.ln()
        pdf.set_font("Helvetica", "", 10)

        for plan in plans:

            ref_number = plan.reference_number or ""
            done = "X"
            name = plan.name or ""
            description = plan.description or ""

            tenants = []

            for action in plan.maintenance_action.all():
                if action.tenant:
                    tenants.append(action.tenant.name)

            tenant = ", ".join(set(tenants))

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

            x = x_start
            for width in col_widths:
                pdf.rect(x, y_start, width, row_height)
                x += width

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

# class MaintenanceActionPlanPDFView(View):

#     LINE_HEIGHT = 6

#     def render_m2m_cell(self, pdf, x, y, width, relation):
#         pdf.set_xy(x, y)

#         if relation is None:
#             return

#         if hasattr(relation, "all"):
#             for obj in relation.all():
#                 pdf.multi_cell(width, self.LINE_HEIGHT, str(obj), border=0, align='C')

#                 y += self.LINE_HEIGHT * self.get_num_lines_for_relation(pdf, str(obj), width)
#                 pdf.set_xy(x, y)
#             return

#         pdf.multi_cell(width, self.LINE_HEIGHT, str(relation), border=0, align='C')

#     def get_relation_text(self, relation):
#         if relation is None:
#             return ""

#         if hasattr(relation, "all"):
#             return "\n".join([str(obj) for obj in relation.all()])

#         return str(relation)

#     def get_num_lines_for_relation(self, pdf, relation, width):
#         if relation is None:
#             return 1

#         if hasattr(relation, "all"):
#             text = "\n".join([str(obj) for obj in relation.all()])
#         else:
#             text = str(relation)

#         lines = 0

#         for paragraph in text.split("\n"):
#             split_lines = pdf.multi_cell(width, self.LINE_HEIGHT, paragraph, border=0, align="C", split_only=True)
#             lines += len(split_lines)

#         return max(1, lines)

#     def get(self, request, *args, **kwargs):
#         parent = kwargs["pk"]

#         actions = MaintenanceTasks.objects.filter(plans_tasks=parent)

#         pdf = MaintenancePlansPDF()
#         pdf.set_auto_page_break(auto=True, margin=15)
#         pdf.add_page()
#         pdf.set_font("Helvetica", size=10)

#         headers = ["Maintenance Windows", "Maintenance Actions", "Virtual Machine", "Comments", "Device"]
#         col_widths = [40, 40, 40, 40, 30]

#         pdf.set_font("Helvetica", "B", 10)
#         for i, header in enumerate(headers):
#             pdf.cell(col_widths[i], 8, header, border=1, align="C")
#         pdf.ln()
#         pdf.set_font("Helvetica", "", 10)

#         for action in actions:

#             x_start = pdf.get_x()
#             y_start = pdf.get_y()

#             lines = []

#             lines.append(self.get_num_lines_for_relation(pdf, action.maintenance_windows, col_widths[0]))

#             lines.append(self.get_num_lines_for_relation(pdf, action.maintenance_action, col_widths[1]))

#             lines.append(self.get_num_lines_for_relation(pdf, action.virtual_machine, col_widths[2]))

#             comments_list = []

#             for vm in action.virtual_machine.all():
#                 if vm.comments:
#                     cleaned = "\n".join(
#                         " ".join(line.split())
#                         for line in vm.comments.splitlines()
#                     )
#                     comments_list.append(cleaned)

#             comments = "\n---VM-SEPARATOR---\n".join(comments_list)
#             lines.append(self.get_num_lines_for_relation(pdf, comments, col_widths[3]))

#             lines.append(self.get_num_lines_for_relation(pdf, action.device, col_widths[4]))

#             row_height = max(lines) * self.LINE_HEIGHT

#             x = x_start
#             for width in col_widths:
#                 pdf.rect(x, y_start, width, row_height)
#                 x += width

#             self.render_m2m_cell(pdf, x_start, y_start, col_widths[0], action.maintenance_windows)
#             self.render_m2m_cell(pdf, x_start + col_widths[0], y_start, col_widths[1], action.maintenance_action)
#             x_vm = x_start + col_widths[0] + col_widths[1]
#             x_comment = x_vm + col_widths[2]

#             current_y = y_start

#             vms = list(action.virtual_machine.all())

#             for index, vm in enumerate(vms):

#                 vm_text = str(vm)
#                 comment_text = vm.comments or ""

#                 vm_lines = pdf.multi_cell(
#                     col_widths[2],
#                     self.LINE_HEIGHT,
#                     vm_text,
#                     split_only=True
#                 )

#                 comment_lines = pdf.multi_cell(
#                     col_widths[3],
#                     self.LINE_HEIGHT,
#                     comment_text,
#                     split_only=True
#                 )

#                 needed_lines = max(len(vm_lines), len(comment_lines))
#                 block_height = needed_lines * self.LINE_HEIGHT

#                 pdf.set_xy(x_vm, current_y)
#                 pdf.multi_cell(
#                     col_widths[2],
#                     self.LINE_HEIGHT,
#                     vm_text,
#                     border=0,
#                     align="C"
#                 )

#                 pdf.set_xy(x_comment, current_y)
#                 pdf.multi_cell(
#                     col_widths[3],
#                     self.LINE_HEIGHT,
#                     comment_text,
#                     border=0,
#                     align="L"
#                 )

#                 current_y += block_height

#                 if index < len(vms) - 1:
#                     pdf.line(x_vm, current_y, x_comment + col_widths[3], current_y)


#             self.render_m2m_cell(
#                 pdf,
#                 x_start + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3],
#                 y_start,
#                 col_widths[4],
#                 action.device
#             )

#             pdf.set_xy(x_start, y_start + row_height)

#         response = HttpResponse(
#             pdf.output(dest="S").encode("latin-1"),
#             content_type="application/pdf",
#         )
        
#         response["Content-Disposition"] = f'attachment; filename=\"planned_actions_{datetime.today()}.pdf\"'
#         return response
    
    
    # maintenance window als überpunkt haben und dann den wichtigen feld wie virtual machine und so weiter mehr platz lassen, 
    # in den plan den button pdf erstellen und als select mit den checkboxen 
