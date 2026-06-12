import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { login as apiLogin } from '@/api/client'
import { TOKEN_KEY } from '@/config'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
  const isAuthenticated = computed(() => !!token.value)

  async function login(username: string, password: string): Promise<void> {
    const access = await apiLogin(username, password)
    token.value = access
    localStorage.setItem(TOKEN_KEY, access)
  }

  function logout(): void {
    token.value = null
    localStorage.removeItem(TOKEN_KEY)
  }

  return { token, isAuthenticated, login, logout }
})
