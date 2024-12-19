from django.shortcuts import render
from .serializers import EmployeeSerializer 
from .models import Employee
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 

# Create your views here.

class EmployeeList(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request, pk):
        employee = Employee.objects.get(employee_id=pk)
        if employee:
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"message":"Employee not found!"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        employee = Employee.objects.get(pk=pk)
        if employee:
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Employee not found!"},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        employee = Employee.objects.get(pk=pk)
        if employee:
            employee.delete()
            return Response({"message":"Deleted!"},status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"Employee not found!"},status=status.HTTP_404_NOT_FOUND)