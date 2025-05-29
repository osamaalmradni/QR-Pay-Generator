# payments/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QRCodeRecordViewSet
from .bank_views import InitiatePaymentView, PaymentStatusView

router = DefaultRouter()
router.register(r'qr', QRCodeRecordViewSet, basename='qrcode')

urlpatterns = [
    path('', include(router.urls)),
    path('bank/initiate/', InitiatePaymentView.as_view(), name='bank_initiate'),
    path('bank/status/', PaymentStatusView.as_view(), name='bank_status'),
]
