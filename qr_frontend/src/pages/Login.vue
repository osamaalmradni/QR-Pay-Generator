<template>
  <q-page class="q-pa-md flex flex-center">
    <q-card style="max-width: 400px; width: 100%">
      <!-- Überschrift für das Login-Formular -->
      <q-card-section>
        <h5>Anmelden</h5>
      </q-card-section>
      <!-- Login-Formular -->
      <q-form @submit.prevent="login">
        <q-card-section>
          <!-- Eingabefeld für den Benutzernamen -->
          <q-input
            v-model="creds.username"
            label="Benutzername"
            filled
            required
          />
          <!-- Eingabefeld für das Passwort -->
          <q-input
            v-model="creds.password"
            label="Passwort"
            type="password"
            filled
            required
          />
        </q-card-section>
        <!-- Button zum Absenden des Formulars -->
        <q-card-actions align="right">
          <q-btn label="Login" type="submit" color="primary" />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-page>
</template>

<script setup>
// Komponentenname für ESLint (mehrwortig)
defineOptions({ name: 'LoginPage' })

import { ref } from 'vue'
import { api } from 'boot/axios'
import { Notify } from 'quasar'
import { useRouter } from 'vue-router'
import { userState } from 'src/stores/userState'

const router = useRouter()
const creds = ref({ username: '', password: '' })

// Login-Funktion: Authentifiziert den Benutzer und speichert das Token
async function login() {
  try {
    const { data } = await api.post('/token/', creds.value)
    localStorage.setItem('accessToken', data.access)
    localStorage.setItem('user', JSON.stringify({ username: creds.value.username }))
    userState.user = { username: creds.value.username }
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
    Notify.create({ type: 'positive', message: 'Erfolgreich angemeldet!' })
    router.push('/') // Nach Login zur Startseite weiterleiten
  }
  catch {
    Notify.create({ type: 'negative', message: 'Login fehlgeschlagen' })
  }
}
</script>
