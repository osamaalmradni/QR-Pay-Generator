<template>
  <q-page class="flex flex-center bg-page">
    <div class="column items-center q-gutter-y-xl" style="width:100%;max-width:480px;">
      <q-card class="q-pa-xl shadow-2" style="border-radius: 16px; width:100%; background: #fff;">
        <q-card-section class="text-center">
          <q-icon name="qr_code" size="56px" color="primary" class="q-mb-md" />
          <div class="text-h5 text-primary text-weight-bold q-mb-xs">
            Generate SEPA QR Code
          </div>
          <div class="text-subtitle2 text-grey-7 q-mb-md">
            Fill in your payment details or select a saved template.
          </div>
        </q-card-section>
        <q-separator />

        <!-- Auswahl eines gespeicherten Templates -->
        <q-card-section>
          <q-select
            v-model="selectedTemplate"
            :options="savedTemplates"
            label="Gespeicherte Vorlagen"
            option-label="name"
            option-value="id"
            emit-value
            map-options
            clearable
            dense
            class="q-mb-md"
            @update:model-value="onTemplateSelect"
          />
          <!-- Buttons zum Bearbeiten oder Löschen der Vorlage -->
          <div v-if="selectedTemplate" class="row q-gutter-sm q-mb-md">
            <q-btn color="secondary" icon="edit" label="Bearbeiten" @click="editTemplate" />
            <q-btn color="negative" icon="delete" label="Löschen" @click="deleteTemplate" />
          </div>
        </q-card-section>

        <!-- Formular für die Eingabe der Zahlungsdaten -->
        <q-card-section>
          <q-form @submit.prevent="generateQr">
            <q-input
              v-model="form.accountHolderName"
              label="Kontoinhaber"
              dense
              outlined
              class="q-mb-md"
              :readonly="!!selectedTemplate"
              required
            />
            <q-input
              v-model="form.iban"
              label="IBAN"
              dense
              outlined
              class="q-mb-md"
              :readonly="!!selectedTemplate"
              required
            />
            <q-input
              v-model="form.swiftBic"
              label="SWIFT/BIC"
              dense
              outlined
              class="q-mb-md"
              :readonly="!!selectedTemplate"
            />
            <q-input
              v-model="form.amount"
              label="Betrag (EUR)"
              type="number"
              dense
              outlined
              class="q-mb-md"
              :readonly="!!selectedTemplate"
              required
            />
            <q-input
              v-model="form.paymentReason"
              label="Verwendungszweck"
              dense
              outlined
              class="q-mb-md"
              :readonly="!!selectedTemplate"
            />
            <!-- Button zum Generieren des QR-Codes -->
            <div class="q-mt-md">
              <q-btn
                color="primary"
                icon="qr_code"
                label="QR-Code generieren"
                type="submit"
                size="lg"
                unelevated
                class="full-width"
                :disable="!!selectedTemplate"
              />
            </div>
            <!-- Buttons zum Leeren des Formulars und zum Speichern der Vorlage -->
            <div class="row items-center q-gutter-sm q-mt-sm">
              <q-btn
                color="secondary"
                icon="clear"
                label="Leeren"
                flat
                class="col"
                @click="clearForm"
                :disable="!!selectedTemplate"
              />
              <q-btn
                color="accent"
                icon="save"
                label="Speichern"
                flat
                class="col"
                @click="saveTemplate"
                :disable="!!form.accountHolderName || !!form.iban ? false : true"
              />
            </div>
          </q-form>
        </q-card-section>

        <q-separator />

        <!-- Anzeige des generierten QR-Codes -->
        <q-card-section class="flex flex-center">
          <div v-if="qrCodeData">
            <q-img
              :src="qrCodeData"
              style="width: 200px; height: 200px;"
              spinner-color="primary"
              spinner-size="40px"
              class="q-mb-sm"
            />
            <div class="text-caption text-grey-7 q-mt-xs">Ihr SEPA QR-Code</div>
          </div>
          <div v-else class="text-grey-5 q-mt-md" style="height: 200px; display: flex; align-items: center;">
            QR-Code wird hier angezeigt
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
// Komponentenname für ESLint
defineOptions({ name: 'GenerateQrPage' })

import { ref, watch } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Formular-Daten für den QR-Code
const form = ref({
  accountHolderName: '',
  iban: '',
  swiftBic: '',
  amount: '',
  paymentReason: ''
})

// QR-Code-Bild (als Data-URL)
const qrCodeData = ref('')

// Gespeicherte Vorlagen aus dem LocalStorage
const savedTemplates = ref(loadTemplates())
const selectedTemplate = ref(null)

// Lädt die Vorlagen aus dem LocalStorage
function loadTemplates() {
  try {
    return JSON.parse(localStorage.getItem('qrTemplates') || '[]')
  } catch {
    return []
  }
}

// Speichert die Vorlagen im LocalStorage
function saveTemplates() {
  localStorage.setItem('qrTemplates', JSON.stringify(savedTemplates.value))
}

// Wird aufgerufen, wenn eine Vorlage ausgewählt wird
function onTemplateSelect(id) {
  const template = savedTemplates.value.find(t => t.id === id)
  if (template) {
    form.value = { ...template }
    generateQr()
  } else {
    clearForm()
  }
}

// Generiert den EPC-QR-Code-String und das QR-Code-Bild
function generateQr() {
  const lines = [
    'BCD',
    '001',
    '1',
    'SCT',
    form.value.swiftBic || '',
    form.value.accountHolderName || '',
    form.value.iban || '',
    form.value.amount ? `EUR${parseFloat(form.value.amount).toFixed(2)}` : '',
    '', // Purpose (optional)
    '', // Remittance (optional)
    form.value.paymentReason || ''
  ]
  const epcString = lines.join('\n')
  qrCodeData.value = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(epcString)}`
}

// Speichert eine neue Vorlage oder aktualisiert eine bestehende
function saveTemplate() {
  $q.dialog({
    title: 'QR-Vorlage speichern',
    message: 'Bitte einen Namen für die Vorlage eingeben:',
    prompt: {
      model: '',
      type: 'text',
      isValid: val => !!val && val.trim().length > 0
    },
    cancel: true,
    persistent: true
  }).onOk(name => {
    // Aktualisieren, wenn eine Vorlage ausgewählt ist
    if (selectedTemplate.value) {
      const idx = savedTemplates.value.findIndex(t => t.id === selectedTemplate.value)
      if (idx !== -1) {
        savedTemplates.value[idx] = { ...form.value, id: selectedTemplate.value, name }
        saveTemplates()
        $q.notify({ type: 'positive', message: 'Vorlage aktualisiert.' })
        return
      }
    }
    // Neue Vorlage speichern
    const id = Date.now()
    savedTemplates.value.push({ ...form.value, id, name })
    saveTemplates()
    selectedTemplate.value = id
    $q.notify({ type: 'positive', message: 'Vorlage gespeichert.' })
  })
}

// Löscht die aktuell ausgewählte Vorlage
function deleteTemplate() {
  if (!selectedTemplate.value) return
  $q.dialog({
    title: 'Vorlage löschen',
    message: 'Möchten Sie diese Vorlage wirklich löschen?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    const idx = savedTemplates.value.findIndex(t => t.id === selectedTemplate.value)
    if (idx !== -1) {
      savedTemplates.value.splice(idx, 1)
      saveTemplates()
      $q.notify({ type: 'positive', message: 'Vorlage gelöscht.' })
      clearForm()
    }
  })
}

// Aktiviert die Bearbeitung der Vorlage (macht die Felder editierbar)
function editTemplate() {
  selectedTemplate.value = null
}

// Setzt das Formular und die Auswahl zurück
function clearForm() {
  form.value = {
    accountHolderName: '',
    iban: '',
    swiftBic: '',
    amount: '',
    paymentReason: ''
  }
  qrCodeData.value = ''
  selectedTemplate.value = null
}

// Beobachtet Änderungen am Formular und setzt den QR-Code zurück, wenn keine Vorlage ausgewählt ist
watch(form, () => {
  if (!selectedTemplate.value) {
    qrCodeData.value = ''
  }
}, { deep: true })
</script>

<style scoped>
.bg-page {
  background: #eaf3fa;
  min-height: 100vh;
}
</style>
