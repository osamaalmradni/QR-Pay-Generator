<template>
  <q-page class="q-pa-md">
    <div class="row justify-center">
      <div class="col-12 col-md-6">
        <q-card flat bordered class="q-pa-md">
          <!-- Überschrift für die Zahlungsübersicht -->
          <q-card-section>
            <h5>Zahlungsdetails überprüfen</h5>
          </q-card-section>

          <q-separator />

          <!-- Anzeige der Zahlungsdaten -->
          <q-card-section class="q-pa-sm">
            <div class="row q-col-gutter-md">
              <div class="col-12">
                <div><strong>Kontoinhaber:</strong> {{ payment.accountHolderName }}</div>
              </div>
              <div class="col-12">
                <div><strong>IBAN:</strong> {{ payment.iban }}</div>
              </div>
              <div class="col-12">
                <div><strong>SWIFT/BIC:</strong> {{ payment.swiftBic }}</div>
              </div>
              <div class="col-12">
                <div><strong>Betrag:</strong> {{ payment.amount }} EUR</div>
              </div>
              <div class="col-12">
                <div><strong>Verwendungszweck:</strong> {{ payment.paymentReason }}</div>
              </div>
            </div>
          </q-card-section>

          <q-separator />

          <!-- Aktions-Buttons: Zurück oder Zahlung simulieren -->
          <q-card-actions align="right">
            <q-btn
              label="Bearbeiten / Neu scannen"
              color="secondary"
              flat
              @click="goBack"
            />
            <q-btn
              :label="loading ? 'Sende...' : 'Zahlung senden'"
              color="primary"
              @click="initiatePayment"
              :disable="loading"
            />
          </q-card-actions>

          <!-- Erfolgsbanner nach Zahlungssimulation -->
          <q-card-section v-if="showSuccess" class="q-mt-md">
            <q-banner class="bg-green-1 text-green">
              Zahlung simuliert! Dies ist nur eine Demo, keine echte Zahlung wurde durchgeführt.
            </q-banner>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
// Komponentenname für ESLint (mehrwortig)
defineOptions({ name: 'BankPage' })

import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const route = useRoute()
const router = useRouter()

// Zahlungsdaten, die angezeigt werden
const payment = ref({
  accountHolderName: '',
  iban: '',
  swiftBic: '',
  amount: '',
  paymentReason: ''
})

// Status für Ladevorgang und Erfolgsmeldung
const loading = ref(false)
const showSuccess = ref(false)

// Lädt die Zahlungsdaten aus den Query-Parametern beim Seitenaufruf
onMounted(() => {
  payment.value = {
    accountHolderName: route.query.accountHolderName || '',
    iban: route.query.iban || '',
    swiftBic: route.query.swiftBic || '',
    amount: route.query.amount || '',
    paymentReason: route.query.paymentReason || ''
  }
})

// Navigiert zurück zur Scan-Seite
function goBack() {
  router.push({ name: 'scan' })
}

// Simuliert die Zahlung und zeigt eine Erfolgsmeldung an
function initiatePayment() {
  showSuccess.value = true
  $q.notify({
    type: 'positive',
    message: 'Simulation: Zahlung erfolgreich! (Dies ist nur eine Demo, keine echte Zahlung wurde durchgeführt.)'
  })
}
</script>
