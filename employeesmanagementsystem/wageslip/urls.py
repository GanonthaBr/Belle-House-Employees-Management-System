

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, ClientViewSet, DesignationViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoices')
router.register(r'clients',ClientViewSet,basename='clients')
router.register(r'designations',DesignationViewSet,basename='designations')

urlpatterns = [
    path('', include(router.urls)),
]