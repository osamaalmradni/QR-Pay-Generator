import uuid
from django.db import models

class QRCodeRecord(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    account_holder_name = models.CharField(max_length=255)
    iban = models.CharField(max_length=34)
    swift_bic = models.CharField(max_length=11, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reason = models.CharField(max_length=140, blank=True)
    sepa_payload = models.TextField()
    qr_image = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        help_text="Generated QR image (PNG) stored on server"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_reason} – {self.iban}"
