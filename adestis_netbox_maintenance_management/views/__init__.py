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
from adestis_netbox_maintenance_management.models import MaintenancePlans
from io import BytesIO
from django.http import HttpResponse
from fpdf import FPDF, HTMLMixin

# def generate_pdf(request, pk):
#     today = date.today()
#     return FileResponse(
#         generate_pdf_file(request, pk), 
#         as_attachment=True,
#         filename=f"{today}_maintenance_plan_{pk}.pdf"
#     )

# def generate_pdf_file(request, pk):
#     plan = MaintenancePlannedActions.objects.get(pk=pk)
#     # Filter: Nur Tasks zu diesem Plan
#     maintenance_tasks = plan.maintenance_tasks.all()

#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)

#     y = 750
#     for task in maintenance_tasks:
#         window = task.maintenance_windows.name if task.maintenance_windows else "-"
#         action = task.maintenance_action.name if task.maintenance_action else "-"
#         vms = ", ".join([str(vm) for vm in task.virtual_machine.all()])
#         devices = ", ".join([str(d) for d in task.device.all()])

#         p.drawString(100, y, f"Window: {window}")
#         p.drawString(100, y - 15, f"Action: {action}")
#         p.drawString(100, y - 30, f"VMs: {vms if vms else '-'}")
#         p.drawString(100, y - 45, f"Devices: {devices if devices else '-'}")

#         y -= 80
#         if y < 50:
#             p.showPage()
#             y = 750

#     p.save()
#     buffer.seek(0)
#     return buffer

class MyFPDF(FPDF, HTMLMixin):
    pass


def export_pdf(request, pk):
    obj = MaintenancePlans.objects.get(pk=pk)

    html = f"""
    <h1>Planned Action: {obj.name}</h1>

    <h3>Description</h3>
    <p>{obj.description}</p>

    <h3>Comments</h3>
    <p>{obj.comments}</p>

    <h3>Tenant</h3>
    <p>{obj.tenant}</p>

    <h3>Maintenance Actions</h3>
    <ul>
        {''.join(f'<li>{a}</li>' for a in obj.maintenance_action.all())}
    </ul>

    <h3>Maintenance Windows</h3>
    <ul>
        {''.join(f'<li>{w}</li>' for w in obj.maintenance_windows.all())}
    </ul>

    <h3>Maintenance Tasks</h3>
    <ul>
        {''.join(f'<li>{t}</li>' for t in obj.maintenance_tasks.all())}
    </ul>

    <h3>Virtual Machines</h3>
    <ul>
        {''.join(f'<li>{vm}</li>' for vm in obj.virtual_machine.all())}
    </ul>

    <h3>Devices</h3>
    <ul>
        {''.join(f'<li>{d}</li>' for d in obj.device.all())}
    </ul>

    <h3>Grouping Key</h3>
    <p>{obj.grouping_key}</p>
    """

    pdf = MyFPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.write_html(html)

    response = HttpResponse(
        pdf.output(dest='S').encode('latin1'),
        content_type='application/pdf'
    )
    response['Content-Disposition'] = f'attachment; filename="{obj.name}.pdf"'

    return response

# Report engine auf html ebene arbeiten statt mit canvas 
# html jinja2 html report pdf 
