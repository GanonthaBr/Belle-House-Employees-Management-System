from django.urls import path

from . import views

urlpatterns = [
    path('employees/', views.EmployeeList.as_view()),
    path('employees/<int:pk>', views.EmployeeView.as_view()),
]