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
    total = SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ['id','topic','name','date','number','echeance','client','client_id','tax','type_tax','payment_mode','designations','montant_avance','total_amount','total','stamp']
        read_only_fields = ['total_amount','total']

    #explicitly define update method
    def update(self,instance,validated_data):
        designation_data = validated_data.pop('designations')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if designation_data:
            for designation in designation_data:
                designation_id = designation.get('id',None)
                if designation_id:
                    designation_obj = Designation.objects.get(id=designation_id,invoice=instance)
                    for attr, value in designation.items():
                        setattr(designation_obj,attr,value)
                        designation_obj.save()
                else:
                    designation_obj = Designation.objects.create(invoice=instance,**designation)


    def get_total(self,obj):
        return obj.total
    def get_total_amount(self,obj):
        return obj.total_amount
    
    def create(self, validated_data):
        designation_data = validated_data.pop('designations')
        invoice = Invoice.objects.create(**validated_data)
        Designation.objects.bulk_create([
            Designation(invoice=invoice, **designation) for designation in designation_data
        ])
        return invoice