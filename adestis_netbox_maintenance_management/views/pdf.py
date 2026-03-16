import os
import tempfile
import subprocess

from django.http import FileResponse
from lxml import etree
from django.template.loader import get_template
from adestis_netbox_maintenance_management.models import MaintenancePlannedActions
from django.conf import settings


def generate_xml(plans):
    """
    Generiert XML aus MaintenancePlannedActions
    next_due_date kommt aus den MaintenanceTasks
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

            # Maintenance Actions
            ma = etree.SubElement(action, "maintenance-actions")
            for a in plan.maintenance_action.all():
                etree.SubElement(ma, "maintenance-action").text = a.name

            # Virtual Machines
            vms = etree.SubElement(action, "vms")

            for vm in plan.virtual_machine.all():
                vmnode = etree.SubElement(vms, "vm")

                etree.SubElement(vmnode, "name").text = vm.name
                etree.SubElement(vmnode, "comment").text = getattr(vm, "comments", "")

            # Devices
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
    plans = MaintenancePlannedActions.objects.prefetch_related(
        "maintenance_tasks",
        "maintenance_action",
        "virtual_machine",
        "device"
    )

    # XML erzeugen
    xml_data = generate_xml(plans)  # deine Funktion bleibt gleich

    # XSLT laden und FO transformieren
    BASE_DIR = settings.BASE_DIR  # Django BASE_DIR
    xslt_path = os.path.join(
        BASE_DIR,
        "adestis_netbox_maintenance_management",
        "templates",
        "planned_actions",
        "planned_actions.xslt"
    )

    xslt_tree = etree.parse(xslt_path)  # <- parse statt XML
    transform = etree.XSLT(xslt_tree)
    transform = etree.XSLT(xslt_tree)
    xml_tree = etree.fromstring(xml_data)
    fo_tree = transform(xml_tree)

    # FO-Datei schreiben
    with tempfile.NamedTemporaryFile(delete=False, suffix=".fo") as fo_file:
        fo_tree.write(
            fo_file.name,
            pretty_print=True,
            encoding="UTF-8",
            xml_declaration=True
        )

    # FO-Datei zum Download als „Pseudo-PDF“
    return FileResponse(
        open(fo_file.name, "rb"),
        content_type="application/pdf",  # PDF, obwohl nur FO drinsteht
        filename="planned_actions.pdf"
    )