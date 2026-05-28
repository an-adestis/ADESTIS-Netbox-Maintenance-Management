from django.http import FileResponse
from django.template.loader import get_template
from lxml import etree
import tempfile
import subprocess
import os

from adestis_netbox_maintenance_management.models import MaintenanceTasks
from django.http import FileResponse, Http404
from django.template.loader import get_template
from lxml import etree
import tempfile
import subprocess
import os

from adestis_netbox_maintenance_management.models import MaintenancePlannedActions

def generate_xml(plan):
    root = etree.Element("planned-actions")

    tasks = plan.maintenance_tasks.all().order_by("next_due_date")

    for task in tasks:
        group = etree.SubElement(root, "group")
        etree.SubElement(group, "next_due_date").text = str(task.next_due_date or "")

        action_el = etree.SubElement(group, "maintenance_action")
        etree.SubElement(action_el, "start_time").text = str(getattr(task, "start_time", "") or "")
        etree.SubElement(action_el, "end_time").text = str(getattr(task, "end_time", "") or "")
        etree.SubElement(action_el, "name").text = task.maintenance_action.name if task.maintenance_action else "—"
        etree.SubElement(action_el, "comments").text = task.comments or ""

        vms_node = etree.SubElement(action_el, "vms")
        for vm in task.virtual_machine.all():
            vm_node = etree.SubElement(vms_node, "vm")
            etree.SubElement(vm_node, "name").text = vm.name
            etree.SubElement(vm_node, "comment").text = getattr(vm, "comments", "") or ""

        devices_node = etree.SubElement(action_el, "devices")
        for device in task.device.all():
            dev_node = etree.SubElement(devices_node, "device")
            etree.SubElement(dev_node, "name").text = device.name
            etree.SubElement(dev_node, "comment").text = ""

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def planned_actions_pdf(request, pk):
    try:
        plan = MaintenancePlannedActions.objects.prefetch_related(
            "maintenance_tasks__virtual_machine",
            "maintenance_tasks__device",
            "maintenance_tasks__maintenance_action",
        ).get(pk=pk)
    except MaintenancePlannedActions.DoesNotExist:
        raise Http404

    xml_data = generate_xml(plan)
    xml_tree = etree.fromstring(xml_data)

    template = get_template("adestis_netbox_maintenance_management/planned_actions.xslt")
    xslt_content = template.template.source.encode("utf-8")
    xslt_tree = etree.XML(xslt_content)
    transform = etree.XSLT(xslt_tree)

    try:
        fo_tree = transform(xml_tree)
    except etree.XSLTApplyError as e:
        print(xml_data.decode("utf-8"))
        raise e

    fo_bytes = etree.tostring(fo_tree, encoding="utf-8", xml_declaration=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".fo") as fo_file, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:

        fo_file.write(fo_bytes)
        fo_file.flush()

        env = os.environ.copy()
        env["JAVA_HOME"] = "/usr/lib/jvm/default-java"

        result = subprocess.run(
            ["java", "-cp", "/usr/share/java/*",
             "org.apache.fop.cli.Main",
             "-fo", fo_file.name,
             "-pdf", pdf_file.name],
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
            filename=f"planned_actions_{plan.name}.pdf",
            as_attachment=True
        )

    os.unlink(fo_file.name)
    os.unlink(pdf_file.name)

    return response