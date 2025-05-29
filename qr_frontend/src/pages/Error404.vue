<template>
  <q-page class="q-pa-md flex flex-center">
    <div>
      <!-- Überschrift für Fehler 404 -->
      <h1>404 – Seite nicht gefunden</h1>
      <!-- Button zur Rückkehr zur Startseite -->
      <q-btn label="Zur Startseite" to="/" color="primary" />
    </div>
  </q-page>
</template>

<script setup>
defineOptions({ name: 'Error404Page' }) // Mehrwort-Komponentenname für ESLint
</script>
