import { reactive } from 'vue'

export const userState = reactive({
  user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null
})