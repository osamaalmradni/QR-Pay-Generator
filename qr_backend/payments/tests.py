from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class QRCodeAPITest(APITestCase):
    def setUp(self):
        # Testbenutzer anlegen und JWT-Token holen
        self.user = User.objects.create_user(username='testuser', password='secret')
        resp = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'testuser', 'password': 'secret'},
            format='json'
        )
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_qr(self):
        url = reverse('qrcode-list')
        data = {
            'account_holder_name': 'Max Mustermann',
            'iban': 'DE89370400440532013000',
            'swift_bic': 'DEUTDEFF',
            'amount': '123.45',
            'payment_reason': 'Testzahlung'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('qr_image', resp.data)

    def test_invalid_iban(self):
        url = reverse('qrcode-list')
        data = {
            'account_holder_name': 'Test',
            'iban': 'INVALID',
            'swift_bic': '',
            'amount': '10.00',
            'payment_reason': ''
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized(self):
        self.client.credentials()  # Kein Token
        url = reverse('qrcode-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

class BankAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bankuser', password='secret')
        resp = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'bankuser', 'password': 'secret'},
            format='json'
        )
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_initiate_payment(self):
        url = reverse('bank_initiate')
        data = {
            'account_holder_name': 'Max Mustermann',
            'iban': 'DE89370400440532013000',
            'swift_bic': 'DEUTDEFF',
            'amount': '50.00',
            'payment_reason': 'Rechnung'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('transaction_id', resp.data)

    def test_payment_status(self):
        from .bank_service import initiate_payment
        result = initiate_payment({})
        transaction_id = result['transaction_id']
        url = f"{reverse('bank_status')}?transaction_id={transaction_id}"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'completed')
