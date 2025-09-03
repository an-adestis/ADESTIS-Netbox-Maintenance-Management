from django.http import HttpResponse
from django.template.loader import get_template
from adestis_netbox_maintenance_management.models.maintenancereports import get_kunden_report_data, get_adestis_report_data
import weasyprint  # falls du PDF erzeugst


from django.views.generic import TemplateView

class MaintenanceReportsListView(TemplateView):
    template_name = 'adestis_netbox_maintenance_management/maintenancereports.html'



def report_pdf_kunde(request, tenant_id):
    context = get_kunden_report_data(tenant_id)
    html = get_template('reports/pdf_kunde.html').render(context)
    pdf = weasyprint.HTML(string=html).write_pdf()
    return HttpResponse(pdf, content_type='application/pdf')

def report_pdf_adestis(request):
    context = get_adestis_report_data()
    html = get_template('reports/pdf_adestis.html').render(context)
    pdf = weasyprint.HTML(string=html).write_pdf()
    return HttpResponse(pdf, content_type='application/pdf')
