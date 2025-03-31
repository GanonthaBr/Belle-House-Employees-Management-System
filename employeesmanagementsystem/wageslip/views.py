from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    def destroy(self, request, *args, **kwargs):
        print("DELETE")
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer()

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    def put(self,request):
        try:
            invoice = self.get_object()
        except Invoice.DoesNotExist:
            return Response({"error":"Invoice not Found"},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def download_pdf(self,request,pk=None):
        try:
            invoice = self.get_object()
        except FileNotFoundError:
            return HttpResponse("File Not Found", status=404)
        template_path = 'invoice_pdf.html'
        logo_path = finders.find('logo.png')
        stamp = finders.find('stamp.png')
        if logo_path:
            logo_path = os.path.abspath(logo_path)
        context = {'invoice': invoice, 'stamp':stamp,'logo_path':logo_path}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{invoice.client.client_name}.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
