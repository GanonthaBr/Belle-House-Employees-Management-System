from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Invoice, Client, Designation
from .serializers import InvoiceSerializer, ClientSerializer, DesignationSerializer
from django.template.loader import get_template

from xhtml2pdf import pisa
from django.http import HttpResponse
from django.contrib.staticfiles import finders
import os

# Create your views here.
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer()
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        invoice = self.get_object()
        template_path = 'invoice_pdf.html'
        logo_path = finders.find('logo.png')
        if logo_path:
            logo_path = os.path.abspath(logo_path)
        context = {'invoice': invoice, 'logo_path':logo_path}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{invoice.client}.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response