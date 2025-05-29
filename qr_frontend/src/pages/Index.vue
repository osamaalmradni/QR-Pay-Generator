<template>
  <q-page class="flex flex-center bg-page">
    <div class="column items-center q-gutter-y-xl" style="width:100%;max-width:420px;">
      <q-card class="q-pa-xl shadow-2" style="border-radius: 16px; width:100%; background: #fff;">
        <!-- Kopfbereich mit Logo und Titel -->
        <q-card-section class="text-center">
          <q-icon name="qr_code_2" size="64px" color="primary" class="q-mb-md" />
          <div class="text-h4 text-primary text-weight-bold q-mb-sm">
            QR Pay Generator
          </div>
          <div class="text-subtitle1 text-grey-7 q-mb-md">
            Erstellen und scannen Sie SEPA-Zahlungs-QR-Codes einfach und sicher.
          </div>
        </q-card-section>
        <q-separator />
        <!-- Hauptaktionen: QR-Code generieren oder scannen -->
        <q-card-actions class="q-mt-lg flex flex-center q-gutter-sm">
          <q-btn
            color="primary"
            icon="qr_code"
            label="QR generieren"
            to="/generate"
            size="lg"
            unelevated
            class="full-width"
            style="max-width: 230px;"
          />
          <q-btn
            color="secondary"
            icon="qr_code_scanner"
            label="QR scannen"
            to="/scan"
            size="lg"
            unelevated
            class="full-width"
            style="max-width: 230px;"
          />
        </q-card-actions>
      </q-card>
      <!-- Fußzeile mit Slogan -->
      <div class="text-caption text-grey-6 q-mt-md">
        &copy; 2025 QR Pay Generator &mdash; Schnell. Sicher. Einfach.
      </div>
    </div>
  </q-page>
</template>

<script setup>
// Komponentenname für ESLint (mehrwortig)
defineOptions({ name: 'HomePage' })
</script>

<style scoped>
/* Hintergrundfarbe für die Startseite */
.bg-page {
  background: #eaf3fa;
  min-height: 100vh;
}
</style>
