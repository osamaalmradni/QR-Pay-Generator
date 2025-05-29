<template>
  <q-page class="q-pa-md bg-page flex flex-center">
    <div class="column items-center q-gutter-y-xl" style="width:100%;max-width:420px;">
      <q-card class="q-pa-lg shadow-2" style="border-radius: 8px; width:100%;">
        <!-- Überschrift und Anleitung -->
        <div class="text-h6 q-mb-md">Scan Payment QR Code</div>
        <div class="text-caption text-grey-7 q-mb-lg">
          Positionieren Sie den SEPA-QR-Code im Rahmen, um ihn zu scannen.
        </div>
        <!-- Start-Button und Kamera-Fehleranzeige -->
        <div v-if="!isScanning && !showConfirmation">
          <q-btn
            color="primary"
            icon="photo_camera"
            label="Start Scannen"
            class="full-width"
            @click="startScan"
          />
          <q-banner v-if="cameraAccess === 'denied'" class="bg-red-1 text-negative q-mt-md">
            Kamerazugriff verweigert. Bitte Kamera-Berechtigungen aktivieren oder Kamera wechseln.
          </q-banner>
        </div>
        <!-- Kamera-Initialisierung und Scan-Ansicht -->
        <div v-else-if="isScanning">
          <q-banner v-if="cameraAccess === 'pending'" class="bg-grey-2 text-grey-8 q-mb-md">
            <q-spinner color="primary" size="24px" class="q-mr-sm" /> Kamera wird initialisiert...
          </q-banner>
          <q-banner v-if="cameraAccess === 'denied'" class="bg-red-1 text-negative q-mb-md">
            Kamerazugriff verweigert. Bitte Kamera-Berechtigungen aktivieren oder Kamera wechseln.
          </q-banner>
          <div v-show="cameraAccess === 'granted'" class="relative-position q-mb-md">
            <!-- Video-Stream für das Scannen -->
            <div id="reader" style="width:340px; height:340px; background:#000"></div>
          </div>
          <div class="row q-gutter-sm q-mt-md">
            <!-- Kamera wechseln, falls mehrere vorhanden -->
            <q-btn
              v-if="cameraCount > 1"
              flat
              color="primary"
              icon="flip_camera_android"
              label="Kamera wechseln"
              @click="switchCamera"
              :disable="cameraAccess === 'pending'"
              class="col"
            />
            <!-- Scan abbrechen -->
            <q-btn
              flat
              color="negative"
              icon="close"
              label="Scan abbrechen"
              @click="stopScan"
              class="col"
            />
          </div>
        </div>
        <!-- Anzeige der gescannten Daten und Bearbeitungsoptionen -->
        <div v-else-if="showConfirmation">
          <q-banner v-if="scanError" class="bg-red-1 text-negative q-mb-md">
            {{ scanError }}
          </q-banner>
          <div class="q-mb-md">
            <div class="text-caption text-grey-7">Kontoinhaber</div>
            <q-input v-model="scannedData.accountHolderName" :readonly="!isEditing" dense />
          </div>
          <div class="q-mb-md">
            <div class="text-caption text-grey-7">IBAN</div>
            <q-input v-model="scannedData.iban" :readonly="!isEditing" dense />
          </div>
          <div class="q-mb-md">
            <div class="text-caption text-grey-7">SWIFT/BIC</div>
            <q-input v-model="scannedData.swiftBic" :readonly="!isEditing" dense />
          </div>
          <div class="q-mb-md">
            <div class="text-caption text-grey-7">Betrag</div>
            <q-input v-model="scannedData.amount" :readonly="!isEditing" type="number" dense />
          </div>
          <div class="q-mb-lg">
            <div class="text-caption text-grey-7">Verwendungszweck</div>
            <q-input v-model="scannedData.paymentReason" :readonly="!isEditing" dense />
          </div>
          <div class="row q-gutter-sm">
            <!-- Weiter zur Zahlung -->
            <q-btn color="primary" class="col" icon="check_circle" label="Zur Zahlung" @click="proceedToPayment" :disable="isEditing" />
            <!-- Erneut scannen -->
            <q-btn flat color="grey-7" class="col" icon="replay" label="Erneut scannen" @click="editOrRescan" :disable="isEditing" />
            <!-- Felder bearbeiten oder speichern -->
            <q-btn flat color="secondary" class="col" :icon="isEditing ? 'save' : 'edit'" :label="isEditing ? 'Speichern' : 'Bearbeiten'" @click="toggleEdit" />
          </div>
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
// Komponentenname für ESLint
defineOptions({ name: 'ScanPage' })

import { ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { Html5Qrcode } from 'html5-qrcode'

const router = useRouter()
const isScanning = ref(false) // Status: Wird gerade gescannt?
const showConfirmation = ref(false) // Status: Zeige Bestätigungsansicht?
const cameraAccess = ref('pending') // Kamera-Zugriffsstatus
const currentCamera = ref('user') // Aktuelle Kamera (user/environment)
const scanError = ref('') // Fehler beim Scannen
const scannedData = ref({
  accountHolderName: '',
  iban: '',
  swiftBic: '',
  amount: '',
  paymentReason: ''
})
const cameraCount = ref(1) // Anzahl der verfügbaren Kameras
const isEditing = ref(false) // Bearbeitungsmodus für Felder
let html5Qr = null // Instanz des QR-Scanners

// Stoppt den Scanner beim Verlassen der Seite
onBeforeUnmount(() => {
  if (html5Qr) html5Qr.stop().catch(()=>{})
})

// Parst die SEPA-QR-Daten aus dem gescannten String
function parseSepaQrData(decoded) {
  const lines = decoded.trim().split('\n').map(l => l.trim())
  if (
    lines.length < 8 ||
    lines[0] !== 'BCD' ||
    (lines[1] !== '001' && lines[1] !== '002') ||
    lines[2] !== '1' ||
    lines[3] !== 'SCT'
  ) return null
  const swiftBic = lines[4]
  const accountHolderName = lines[5]
  const iban = lines[6]
  const amountString = lines[7]
  const paymentReason = lines.length > 10 ? lines[10] : ''
  if (!accountHolderName || !iban || !amountString || !amountString.toUpperCase().startsWith('EUR')) return null
  const amountValue = parseFloat(amountString.substring(3))
  if (isNaN(amountValue) || amountValue <= 0) return null
  return { accountHolderName, iban, swiftBic, amount: amountValue, paymentReason }
}

// Startet den Scanvorgang
function startScan() {
  console.log("startScan: called");
  scanError.value = ''
  isScanning.value = true
  cameraAccess.value = 'pending'
  showConfirmation.value = false

  setTimeout(() => {
    const readerDiv = document.getElementById('reader')
    if (readerDiv) {
      readerDiv.innerHTML = ''
      try {
        html5Qr = new Html5Qrcode("reader")
        html5Qr.start(
          { facingMode: "user" },
          { fps: 15, qrbox: 320 },
          (decodedText) => {
            console.log("QR decoded:", decodedText)
            // SEPA-QR-Daten analysieren
            const parsed = parseSepaQrData(decodedText)
            if (parsed) {
              scannedData.value = parsed
              showConfirmation.value = true
              isScanning.value = false
              cameraAccess.value = 'pending'
            } else {
              scanError.value = 'Kein gültiger SEPA-Zahlungs-QR-Code erkannt. Bitte erneut versuchen.'
            }
            html5Qr.stop().then(() => { html5Qr = null })
          }
        ).then(() => {
          cameraAccess.value = 'granted'
        }).catch((err) => {
          scanError.value = 'Kamera-Fehler: ' + err
          cameraAccess.value = 'denied'
        })
      } catch (e) {
        scanError.value = 'Kamera-Fehler: ' + e
        cameraAccess.value = 'denied'
      }
    }
  }, 100)
}

// Stoppt den Scanvorgang und die Kamera
function stopScan() {
  console.log("stopScan: called")
  isScanning.value = false
  cameraAccess.value = 'pending'
  scanError.value = ''
  if (html5Qr) {
    html5Qr.stop().then(() => {
      console.log("stopScan: camera stopped")
      html5Qr = null // Scanner-Instanz leeren
    }).catch((e) => {
      console.warn("stopScan: Fehler beim Stoppen der Kamera", e)
      html5Qr = null // Scanner-Instanz auch bei Fehler leeren
    })
  }
}

// Wechselt zwischen Front- und Rückkamera
function switchCamera() {
  currentCamera.value = currentCamera.value === 'user' ? 'environment' : 'user'
  scanError.value = ''
}

// Leitet zur Zahlungsseite weiter und übergibt die Daten
function proceedToPayment() {
  const params = new URLSearchParams({
    accountHolderName: scannedData.value.accountHolderName,
    iban: scannedData.value.iban,
    swiftBic: scannedData.value.swiftBic,
    amount: scannedData.value.amount,
    paymentReason: scannedData.value.paymentReason
  }).toString()
  router.push(`/bank?${params}`)
}

// Startet einen neuen Scanvorgang
function editOrRescan() {
  showConfirmation.value = false
  scannedData.value = {
    accountHolderName: '',
    iban: '',
    swiftBic: '',
    amount: '',
    paymentReason: ''
  }
  startScan()
}

// Aktiviert/Deaktiviert den Bearbeitungsmodus für die Felder
function toggleEdit() {
  isEditing.value = !isEditing.value
}
</script>

<style scoped>
/* Hintergrundfarbe für die Seite */
.bg-page {
  background: #eaf3fa;
  min-height: 100vh;
}
/* Overlay für den Scanbereich */
.scan-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
/* Rahmen für den Scanbereich */
.scan-box {
  position: absolute;
  top: 12.5%;
  left: 12.5%;
  width: 75%;
  height: 75%;
  border: 2px dashed #fff;
  border-radius: 8px;
  opacity: 0.7;
}
/* Animierte Scanlinie */
.scan-line {
  position: absolute;
  top: 50%;
  left: 13%;
  width: 74%;
  height: 3px;
  background: #e53935;
  opacity: 0.7;
  animation: scan-move 1.5s linear infinite alternate;
  border-radius: 2px;
}
@keyframes scan-move {
  0% { top: 20%; }
  100% { top: 80%; }
}
/* Stil für das Videoelement im Scanbereich */
::v-deep video {
  border: 3px solid red !important;
  z-index: 10000 !important;
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  background: #000 !important;
  opacity: 1 !important;
}
</style>
