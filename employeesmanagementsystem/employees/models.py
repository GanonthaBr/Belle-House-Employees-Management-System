from django.db import models

# Create your models here.
class Employee(models.Model):
    id  = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    hire_date = models.DateField()
    employee_address = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    employee_nationality = models.CharField(max_length=100)