<template>
  <q-layout view="hHh lpR fFf">
    <!-- Kopfzeile mit Navigation und Benutzeraktionen -->
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <!-- Titel der Anwendung, klickbar für Rückkehr zur Startseite -->
        <q-toolbar-title
          class="text-weight-bold cursor-pointer"
          @click="$router.push('/')"
          style="user-select: none;"
        >
          QR Pay Generator
        </q-toolbar-title>
        <div class="q-gutter-sm">
          <!-- Navigationsbutton: QR-Code generieren -->
          <q-btn
            flat
            dense
            round
            icon="qr_code"
            label="Generate"
            to="/generate"
            class="text-white"
          />
          <!-- Navigationsbutton: QR-Code scannen -->
          <q-btn
            flat
            dense
            round
            icon="qr_code_scanner"
            label="Scan"
            to="/scan"
            class="text-white"
          />
          <!-- Login-Button, wenn kein Benutzer angemeldet ist -->
          <template v-if="!userState.user">
            <q-btn
              flat
              dense
              icon="login"
              label="Login"
              to="/login"
              class="text-white"
            />
          </template>
          <!-- Benutzer-Menü, wenn ein Benutzer angemeldet ist -->
          <template v-else>
            <q-btn
              flat
              dense
              class="text-white"
              :label="userState.user.username"
              icon="account_circle"
              dropdown
            >
              <!-- Dropdown-Menü für Benutzeraktionen -->
              <q-menu>
                <q-list>
                  <!-- Abmelden-Option -->
                  <q-item clickable v-close-popup @click="logout">
                    <q-item-section>
                      Abmelden
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </template>
        </div>
      </q-toolbar>
    </q-header>
    <!-- Hauptinhalt der Seite -->
    <q-page-container>
      <router-view />
    </q-page-container>
    <!-- Fußzeile mit rechtlichen Links -->
    <q-footer class="bg-grey-2 text-black">
      <q-toolbar>
        <q-toolbar-title class="footer-title">
          © 2025 QR Pay Generator
        </q-toolbar-title>
        <!-- Link zum Impressum -->
        <q-btn flat label="Impressum" to="/imprint" />
        <!-- Link zum Datenschutz -->
        <q-btn flat label="Datenschutz" to="/privacy" />
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup>
// Importiere Router für Navigation
import { useRouter } from 'vue-router'
// Importiere globalen Benutzerstatus
import { userState } from 'src/stores/userState'

const router = useRouter()

// Funktion zum Abmelden des Benutzers
function logout() {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('user')
  userState.user = null
  router.replace('/login')
}
</script>

<style scoped>
/* Stil für den Titel in der Toolbar */
.q-toolbar-title {
  font-size: 1.4rem;
  letter-spacing: 1px;
}
/* Abstand zwischen den Buttons in der Toolbar */
.q-gutter-sm > * {
  margin-left: 8px !important;
}
/* Stil für kleinere Fußzeile */
.q-footer {
  min-height: 36px;
  padding-top: 4px;
  padding-bottom: 4px;
}
.q-footer .q-toolbar {
  min-height: 32px;
  padding-top: 0;
  padding-bottom: 0;
  color: #727272;
}
.q-footer .q-btn {
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  color: #727272;
  font-weight: 500;
  text-transform: uppercase;
}
.footer-title {
  font-size: 0.75rem !important;
  letter-spacing: 0.5px;
  color: #727272;
  font-weight: 500;
  text-transform: uppercase;
}
</style>
