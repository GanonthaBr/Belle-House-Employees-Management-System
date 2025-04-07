from django.urls import path,include
from . import views
from .views import EmployeeList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'employees',EmployeeList,basename='employees')

urlpatterns = [
    path('', include(router.urls)),
    path('employees/<int:pk>', views.EmployeeView.as_view()),
]