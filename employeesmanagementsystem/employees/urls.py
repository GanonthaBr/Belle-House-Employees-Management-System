from django.urls import path,include
from . import views
from .views import EmployeeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'employees',EmployeeViewSet,basename='employees')

urlpatterns = [
    path('', include(router.urls)),
    # path('employees/<int:pk>', views.EmployeeView.as_view()),
]