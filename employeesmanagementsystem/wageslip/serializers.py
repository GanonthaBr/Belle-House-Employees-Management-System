from .models import Client, Invoice, Designation
from rest_framework import serializers
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
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),source='client',write_only=True
    )
    designations = DesignationSerializer(many=True)
    total_amount = SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ['id','topic','name','date','number','echeance','client','client_id','tax','type_tax','payment_mode','designations','total_amount']
    
    def get_total_amount(self,obj):
        return obj.total_amount
    
    def create(self, validated_data):
        designation_data = validated_data.pop('designations')
        invoice = Invoice.objects.create(**validated_data)
        Designation.objects.bulk_create([
            Designation(invoice=invoice, **designation) for designation in designation_data
        ])
        return invoice