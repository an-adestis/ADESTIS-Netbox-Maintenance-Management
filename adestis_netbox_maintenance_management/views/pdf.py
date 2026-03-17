from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.units import cm
from adestis_netbox_maintenance_management.models import MaintenancePlannedActions
from lxml import etree
import os

def header_footer(canvas, doc):
    # Logo oben rechts
    logo_path = os.path.abspath('path/to/logo.png')  # Pfad zu deinem Logo, absolut oder relativ zum Projekt
    if os.path.exists(logo_path):
        canvas.drawImage(logo_path, doc.width + doc.leftMargin - 3*cm, doc.height + doc.topMargin - 1*cm, width=2.5*cm, height=1*cm)

    # Titel links oben
    canvas.setFont("Helvetica-Bold", 16)
    canvas.setFillColor(colors.HexColor("#3a72a8"))
    canvas.drawString(doc.leftMargin, doc.height + doc.topMargin - 0.8*cm, "Planned Actions")

    # Fußzeile: Seitenzahl rechts unten
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    page_number_text = f"Seite {doc.page} / {{}}"
    canvas.drawRightString(doc.width + doc.leftMargin, 1*cm, page_number_text)

def planned_actions_pdf(request):
    plans = MaintenancePlannedActions.objects.prefetch_related(
        "maintenance_tasks", "maintenance_action", "virtual_machine", "device"
    )

    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=A4,
                          leftMargin=2*cm, rightMargin=2*cm,
                          topMargin=3*cm, bottomMargin=2*cm)

    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height - 2*cm, id='normal')

    template = PageTemplate(id='test', frames=frame, onPage=header_footer)
    doc.addPageTemplates([template])

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.spaceAfter = 6

    story = []

    for plan in plans:
        for task in plan.maintenance_tasks.all().order_by("next_due_date"):
            # Datum als Abschnittsüberschrift
            story.append(Paragraph(f"Datum: {task.next_due_date}", styles['Heading3']))
            story.append(Spacer(1, 6))

            # Startzeit und Endzeit aus dem Task, wenn leer -> ''
            start_time = task.start_time if getattr(task, 'start_time', None) else ''
            end_time = task.end_time if getattr(task, 'end_time', None) else ''

            # Tabellenkopf
            data = [
                ['Startzeit', 'Endzeit', 'Maintenance Action'],
                [start_time, end_time, task.name or '']  # Task-Name statt Plan-Name
            ]

            # VMs als Untertabelle
            vm_data = [['VM', 'Info']]
            for vm in plan.virtual_machine.all():
                vm_data.append([vm.name or '', vm.comments or ''])

            vm_table = Table(vm_data, colWidths=[6*cm, 10*cm])
            vm_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
                ('GRID', (0, 0), (1, 1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ]))

            # Devices als Untertabelle
            device_data = [['Device', 'Info']]
            for device in plan.device.all():
                device_data.append([device.name or '', device.comments or ''])

            device_table = Table(device_data, colWidths=[6*cm, 10*cm])
            device_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))

            # Verschachtelte Tabelle für Kommentare + VMs + Devices
            comments = plan.comments or ''
            nested_table = Table([
                [Paragraph(comments, normal_style)],
                [vm_table],
                [device_table]
            ], colWidths=[16*cm])

            nested_table.setStyle(TableStyle([
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))

            # Leere Zellen bei Startzeit/Endzeit und dann verschachtelte Tabelle in Maintenance Action Spalte
            data.append(['', '', nested_table])

            main_table = Table(data, colWidths=[3*cm, 3*cm, 10*cm], repeatRows=1)
            main_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0a6c86')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ]))

            story.append(main_table)
            story.append(Spacer(1, 24))

    doc.build(story)

    buffer.seek(0)
    return FileResponse(buffer, content_type='application/pdf', filename='planned_actions.pdf')