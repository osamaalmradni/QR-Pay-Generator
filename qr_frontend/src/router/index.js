// src/router/index.js

import { route } from 'quasar/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory
} from 'vue-router'

import routes from './routes'  // Importiert die Routen-Definitionen

export default route(function (/* { store, ssrContext } */) {
  // Wählt den passenden History-Modus (SSR, history, hash)
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory)

  const router = createRouter({
    // Erstellt den Router mit dem gewählten History-Modus und den Routen
    history: createHistory(process.env.VUE_ROUTER_BASE),
    routes, // Array der Seitenrouten
    scrollBehavior: () => ({ left: 0, top: 0 }) // Scrollt bei jedem Seitenwechsel nach oben
  })

  // Navigation Guard: Prüft Login-Status vor jedem Seitenwechsel
  router.beforeEach((to, from, next) => {
    const isLoggedIn = !!localStorage.getItem('accessToken')
    if (to.path !== '/login' && !isLoggedIn) {
      // Wenn nicht eingeloggt und nicht auf Login-Seite → Weiterleitung zu Login
      next('/login')
    } else if (to.path === '/login' && isLoggedIn) {
      // Wenn eingeloggt und auf Login-Seite → Weiterleitung zur Startseite
      next('/')
    } else {
      // Sonst Navigation erlauben
      next()
    }
  })

  return router
})
