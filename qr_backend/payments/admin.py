from django.contrib import admin
from .models import QRCodeRecord

@admin.register(QRCodeRecord)
class QRCodeRecordAdmin(admin.ModelAdmin):
    list_display = ('payment_reason', 'iban', 'amount', 'created_at')
    search_fields = ('payment_reason', 'iban', 'account_holder_name')
    readonly_fields = ('id', 'created_at', 'sepa_payload')
