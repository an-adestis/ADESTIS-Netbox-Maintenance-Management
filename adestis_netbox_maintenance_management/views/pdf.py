from io import BytesIO
from django.http import FileResponse
from adestis_netbox_maintenance_management.models import MaintenancePlannedActions
from lxml import etree
import tempfile
import subprocess
from django.template.loader import get_template

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
import os
from lxml import etree
from importlib import resources
import subprocess
import tempfile
from django.http import FileResponse
from django.contrib.staticfiles import finders
from django.conf import settings

def planned_actions_pdf(request):
    plans = MaintenancePlannedActions.objects.prefetch_related(
        "maintenance_tasks", "maintenance_action", "virtual_machine", "device"
    )

    xml_data = generate_xml(plans)
    xml_tree = etree.fromstring(xml_data)

    # ✅ XSLT über Django Template laden
    template = get_template(
        "adestis_netbox_maintenance_management/planned_actions.xslt"
    )
    xslt_content = template.template.source.encode("utf-8")

    xslt_tree = etree.XML(xslt_content)
    transform = etree.XSLT(xslt_tree)

    fo_tree = transform(xml_tree)
    fo_bytes = etree.tostring(fo_tree, encoding="utf-8", xml_declaration=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".fo") as fo_file, \
        tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:

        fo_file.write(fo_bytes)
        fo_file.flush()

        env = os.environ.copy()
        env["JAVA_HOME"] = "/usr/lib/jvm/default-java"  # hier setzen

        result = subprocess.run(
            ["/usr/bin/fop", "-fo", fo_file.name, "-pdf", pdf_file.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env  # ENV an den subprocess übergeben
        )

        if result.returncode != 0:
            raise Exception("FOP ERROR:\n" + result.stderr)

        return FileResponse(
            open(pdf_file.name, "rb"),
            content_type="application/pdf",
            filename="planned_actions.pdf"
        )