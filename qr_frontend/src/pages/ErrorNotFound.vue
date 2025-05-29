<template>
  <div class="fullscreen bg-blue text-white text-center q-pa-md flex flex-center">
    <div>
      <!-- Fehlercode 404 groß anzeigen -->
      <div style="font-size: 30vh">
        404
      </div>

      <!-- Fehlermeldung für nicht gefundene Seite -->
      <div class="text-h2" style="opacity:.4">
        Oops. Diese Seite existiert nicht...
      </div>

      <!-- Button zur Rückkehr zur Startseite -->
      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="blue"
        unelevated
        to="/"
        label="Zur Startseite"
        no-caps
      />
    </div>
  </div>
</template>

<script setup>
// Keine zusätzliche Logik notwendig
</script>
