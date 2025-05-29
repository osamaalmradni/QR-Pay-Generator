import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Erstellt eine Axios-Instanz mit Basis-URL und Timeout
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 5000
})

export default boot(({ app }) => {
  // Wenn ein Token im LocalStorage vorhanden ist, setze es als Authorization-Header
  const token = localStorage.getItem('accessToken')
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
  // Macht die Axios-Instanz global als this.$api verfügbar
  app.config.globalProperties.$api = api
})

// Exportiert die Axios-Instanz für den Import mit: import { api } from 'boot/axios'
export { api }
