// src/router/routes.js

export default [
  {
    path: '/',                        // Hauptpfad der Anwendung
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',                     // Startseite (Index)
        name: 'home',
        component: () => import('pages/Index.vue')
      },
      {
        path: 'login',                // Login-Seite
        name: 'login',
        component: () => import('pages/Login.vue')
      },
      {
        path: 'generate',             // Seite zum Erstellen von QR-Codes
        name: 'generate',
        component: () => import('pages/Generate.vue')
      },
      {
        path: 'scan',                 // Seite zum Scannen von QR-Codes
        name: 'scan',
        component: () => import('pages/Scan.vue')
      },
      {
        path: 'bank',                 // Zahlungsübersicht nach Scan
        name: 'bank',
        component: () => import('pages/Bank.vue')
      }
    ]
  },
  {
    path: '/:catchAll(.*)*',          // Fängt alle nicht definierten Routen ab (404)
    name: 'error404',
    component: () => import('pages/ErrorNotFound.vue')
  }
]
