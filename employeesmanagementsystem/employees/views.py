from django.shortcuts import render
from .serializers import EmployeeSerializer 
from .models import Employee
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_object(self):
        # Fetch the custom field value from the URL
        lookup_field_value = self.kwargs.get('employee_id')  # Replace 'employee_code' with your field name
        try:
            # Retrieve the employee using the custom field
            return Employee.objects.get(employee_id=lookup_field_value)
        except:
            raise Response({"error": "Employee not found!"}, status=status.HTTP_404_NOT_FOUND)

    # def get(self, request, pk):
    #     employee = Employee.objects.get(employee_id=pk)
    #     if employee:
    #         serializer = EmployeeSerializer(employee)
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     return Response({"message":"Employee not found!"},status=status.HTTP_404_NOT_FOUND)
    
    # def post(self,request):
    #     serializer = EmployeeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, pk):
    #     employee = Employee.objects.get(pk=pk)
    #     if employee:
    #         data = request.data.copy()
    #         data.pop('employee_id', None)  # Exclude employee_id from the update
    #         serializer = EmployeeSerializer(employee, data=data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"message":"Employee not found!"},status=status.HTTP_404_NOT_FOUND)
    
    # def delete(self, request, pk):
    #     employee = Employee.objects.get(pk=pk)
    #     if employee:
    #         employee.delete()
    #         return Response({"message":"Deleted!"},status=status.HTTP_204_NO_CONTENT)
    #     return Response({"message":"Employee not found!"},status=status.HTTP_404_NOT_FOUND)
    

class EmployeeList(APIView):
     def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)