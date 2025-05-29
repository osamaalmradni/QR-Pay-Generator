from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .bank_service import initiate_payment, check_status

class InitiatePaymentView(APIView):
    """
    POST /api/bank/initiate/
    Leitet eine simulierte Zahlung ein.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = initiate_payment(request.data)
        return Response(result, status=status.HTTP_200_OK)

class PaymentStatusView(APIView):
    """
    GET /api/bank/status/?transaction_id=...
    Fragt den Status einer simulierten Zahlung ab.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transaction_id = request.query_params.get('transaction_id')
        if not transaction_id:
            return Response(
                {"detail": "Transaktions-ID fehlt"},
                status=status.HTTP_400_BAD_REQUEST
            )
        result = check_status(transaction_id)
        return Response(result, status=status.HTTP_200_OK)
