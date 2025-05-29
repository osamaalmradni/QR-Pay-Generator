# payments/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import QRCodeRecord
from .serializers import QRCodeRecordSerializer

class QRCodeRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet für CRUD-Operationen an QRCodeRecord:
    - Erstellen (create)
    - Auflisten (list)
    - Detail anzeigen (retrieve)
    - Aktualisieren (update, partial_update)
    - Löschen (destroy)
    """
    queryset = QRCodeRecord.objects.all().order_by('-created_at')
    serializer_class = QRCodeRecordSerializer
    permission_classes = [IsAuthenticated]
