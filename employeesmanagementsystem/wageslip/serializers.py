from .models import Client, Invoice, Designation
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        

class DesignationSerializer(ModelSerializer):
    designation_price = SerializerMethodField()
    class Meta:
        model = Designation
        fields = ['designation_title','designation_details','designation_unit_price','designation_quantity','designation_price']
        read_only_fields = ['designation_price']
    def get_designation_price(self,obj):
        return obj.designation_price
    
class InvoiceSerializer(ModelSerializer):
    designations = DesignationSerializer(many=True)
    total_amount = SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ['topic','number','echeance','client','tax','type_tax','payment_mode','designations','total_amount']
    
    def get_total_amount(self,obj):
        return obj.total_amount
    
    def create(self, validated_data):
        designation_data = validated_data.pop('designations')
        invoice = Invoice.objects.create(**validated_data)
        for designation in designation_data:
            Designation.objects.create(invoice=invoice,**designation)
        return invoice