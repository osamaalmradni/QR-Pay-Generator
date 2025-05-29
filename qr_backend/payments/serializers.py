# payments/serializers.py

from rest_framework import serializers
from stdnum import iban as stdnum_iban
import qrcode
import io
from django.core.files.base import ContentFile
from .models import QRCodeRecord

class QRCodeRecordSerializer(serializers.ModelSerializer):
    """
    Serialisierer für QRCodeRecord.
    Übernimmt Validierung, SEPA-Payload-Erstellung und QR-Code-Generierung.
    """
    qr_image = serializers.ImageField(read_only=True)

    class Meta:
        model = QRCodeRecord
        fields = [
            'id',
            'account_holder_name',
            'iban',
            'swift_bic',
            'amount',
            'payment_reason',
            'sepa_payload',
            'qr_image',
            'created_at',
        ]
        read_only_fields = ('id', 'sepa_payload', 'qr_image', 'created_at')

    def validate_iban(self, value):
        """
        Validiert die IBAN mit python-stdnum und entfernt Leerzeichen.
        """
        if not stdnum_iban.is_valid(value):
            raise serializers.ValidationError("Ungültige IBAN")
        return stdnum_iban.compact(value)

    def _build_sepa_payload(self, data):
        """
        Baut den SEPA-Textkörper mit CR+LF und exakt einer Leerzeile vor dem Zahlungsgrund.
        """
        lines = [
            "BCD",                              # Dienst-Tag
            "001",                              # Version
            "1",                                # Zeichensatz UTF-8
            "SCT",                              # SEPA Credit Transfer
            data['swift_bic'].strip(),         # BIC
            data['account_holder_name'].strip(),# Kontoinhaber
            data['iban'].strip(),               # IBAN
            f"EUR{data['amount']:.2f}",         # Betrag
            "",                                 # Leerzeile (Purpose-Feld)
            data['payment_reason'].strip(),     # Unstrukturierte Information
        ]
        return "\r\n".join(lines) + "\r\n"

    def create(self, validated_data):
        """
        Erzeugt einen neuen QRCodeRecord, generiert das SEPA-Payload,
        erzeugt ein QR-Code-Bild und speichert beides.
        """
        payload_text = self._build_sepa_payload(validated_data)
        record = QRCodeRecord.objects.create(
            account_holder_name=validated_data['account_holder_name'],
            iban=validated_data['iban'],
            swift_bic=validated_data.get('swift_bic', ''),
            amount=validated_data['amount'],
            payment_reason=validated_data.get('payment_reason', ''),
            sepa_payload=payload_text,
        )

        # QR-Code generieren und als PNG speichern
        qr_img = qrcode.make(payload_text)
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        filename = f"{record.id}.png"
        record.qr_image.save(filename, ContentFile(buffer.read()), save=True)
        return record

    def update(self, instance, validated_data):
        """
        Aktualisiert Felder eines bestehenden QRCodeRecord,
        regeneriert das SEPA-Payload und das QR-Code-Bild.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        payload_text = self._build_sepa_payload(validated_data)
        instance.sepa_payload = payload_text

        qr_img = qrcode.make(payload_text)
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        filename = f"{instance.id}.png"
        instance.qr_image.save(filename, ContentFile(buffer.read()), save=True)

        instance.save()
        return instance
