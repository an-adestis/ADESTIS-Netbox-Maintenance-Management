from django.http import FileResponse
from django.template.loader import get_template
from lxml import etree
import tempfile
import subprocess
import os

from adestis_netbox_maintenance_management.models import MaintenancePlannedActions

def generate_xml(plans):
    root = etree.Element("planned-actions")

    for plan in plans:
        tasks = plan.maintenance_tasks.all().order_by("next_due_date")
        for task in tasks:
            group = etree.SubElement(root, "group")
            group.set("date", str(task.next_due_date or ""))

            actions = list(plan.maintenance_action.all())
            if not actions:
                # Wenn keine Actions existieren, Dummy-Action hinzufügen
                actions = [None]

            for action_data in actions:
                action = etree.SubElement(group, "action")
                etree.SubElement(action, "start-time").text = str(getattr(task, "start_time", ""))
                etree.SubElement(action, "end-time").text = str(getattr(task, "end_time", ""))
                etree.SubElement(action, "name").text = action_data.name if action_data else "—"
                etree.SubElement(action, "comments").text = plan.comments or "—"

                # VMs
                vms_node = etree.SubElement(action, "vms")
                for vm in plan.virtual_machine.all():
                    vm_node = etree.SubElement(vms_node, "vm")
                    etree.SubElement(vm_node, "name").text = vm.name
                    etree.SubElement(vm_node, "comment").text = getattr(vm, "comments", "")

                # Devices
                devices_node = etree.SubElement(action, "devices")
                for device in plan.device.all():
                    dev_node = etree.SubElement(devices_node, "device")
                    etree.SubElement(dev_node, "name").text = device.name
                    etree.SubElement(dev_node, "comment").text = ""

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def planned_actions_pdf(request):
    plans = MaintenancePlannedActions.objects.prefetch_related(
        "maintenance_tasks", "maintenance_action", "virtual_machine", "device"
    )

    xml_data = generate_xml(plans)
    xml_tree = etree.fromstring(xml_data)

    # XSLT laden
    template = get_template("adestis_netbox_maintenance_management/planned_actions.xslt")
    xslt_content = template.template.source.encode("utf-8")
    xslt_tree = etree.XML(xslt_content)
    transform = etree.XSLT(xslt_tree)

    # Transformation
    try:
        fo_tree = transform(xml_tree)
    except etree.XSLTApplyError as e:
        # XML debug output
        print(xml_data.decode("utf-8"))
        raise e

    fo_bytes = etree.tostring(fo_tree, encoding="utf-8", xml_declaration=True)

    # FO → PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".fo") as fo_file, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:

        fo_file.write(fo_bytes)
        fo_file.flush()

        env = os.environ.copy()
        env["JAVA_HOME"] = "/usr/lib/jvm/default-java"  # ggf. anpassen

        result = subprocess.run(
            [
                "java",
                "-cp",
                "/usr/share/java/*",
                "org.apache.fop.cli.Main",
                "-fo",
                fo_file.name,
                "-pdf",
                pdf_file.name
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        if not os.path.exists(pdf_file.name) or os.path.getsize(pdf_file.name) == 0:
            raise Exception(
                f"FOP ERROR:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        response = FileResponse(
            open(pdf_file.name, "rb"),
            content_type="application/pdf",
            filename="planned_actions.pdf",
            as_attachment=True
        )

    os.unlink(fo_file.name)
    os.unlink(pdf_file.name)

    return response