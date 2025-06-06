# Generated by Django 5.2.1 on 2025-05-26 11:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QRCodeRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('account_holder_name', models.CharField(max_length=255)),
                ('iban', models.CharField(max_length=34)),
                ('swift_bic', models.CharField(blank=True, max_length=11)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_reason', models.CharField(blank=True, max_length=140)),
                ('sepa_payload', models.TextField()),
                ('qr_image', models.ImageField(blank=True, help_text='Generated QR image (PNG) stored on server', upload_to='qr_codes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
