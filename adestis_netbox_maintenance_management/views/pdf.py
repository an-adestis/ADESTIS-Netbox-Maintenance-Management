from io import BytesIO
from django.http import FileResponse
from adestis_netbox_maintenance_management.models import MaintenancePlannedActions
from lxml import etree
from django.http import HttpResponse
import tempfile
from django.conf import settings
from django.template.loader import get_template
import tempfile
from weasyprint import HTML
def generate_xml(plans):
    """
    Generiert XML aus MaintenancePlannedActions
    """
    root = etree.Element("planned-actions")

    for plan in plans:
        tasks = plan.maintenance_tasks.all().order_by("next_due_date")
        for task in tasks:
            group = etree.SubElement(root, "group")
            group.set("date", str(task.next_due_date or ""))

            action = etree.SubElement(group, "action")
            etree.SubElement(action, "name").text = plan.name
            etree.SubElement(action, "comments").text = plan.comments or ""

            ma = etree.SubElement(action, "maintenance-actions")
            for a in plan.maintenance_action.all():
                etree.SubElement(ma, "maintenance-action").text = a.name

            vms = etree.SubElement(action, "vms")
            for vm in plan.virtual_machine.all():
                vmnode = etree.SubElement(vms, "vm")
                etree.SubElement(vmnode, "name").text = vm.name
                etree.SubElement(vmnode, "comment").text = getattr(vm, "comments", "")

            devices = etree.SubElement(action, "devices")
            for d in plan.device.all():
                dev = etree.SubElement(devices, "device")
                etree.SubElement(dev, "name").text = d.name
                etree.SubElement(dev, "comment").text = ""

    return etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )


def planned_actions_pdf(request):
    """
    Generiert PDF aus XML/XSLT und liefert es direkt zum Download
    """
    plans = MaintenancePlannedActions.objects.prefetch_related(
        "maintenance_tasks",
        "maintenance_action",
        "virtual_machine",
        "device"
    )
    xml_data = generate_xml(plans)
    xml_tree = etree.fromstring(xml_data)

    # XSLT für HTML laden
    from django.template.loader import get_template
    template = get_template(
        "adestis_netbox_maintenance_management/planned_actions/planned_actions.xslt"
    )
    xslt_content = template.render({}).encode("utf-8")
    xslt_tree = etree.XML(xslt_content)
    transform = etree.XSLT(xslt_tree)

    # XML → HTML transformieren
    html_tree = transform(xml_tree)
    html_string = etree.tostring(html_tree, encoding="unicode", method="html")

    # HTML → PDF mit WeasyPrint
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        HTML(string=html_string).write_pdf(pdf_file.name)

    # PDF direkt zum Download ausliefern
    return FileResponse(
        open(pdf_file.name, "rb"),
        content_type="application/pdf",
        filename="planned_actions.pdf"
    )