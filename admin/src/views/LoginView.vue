<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

async function submit(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    await auth.login(username.value, password.value)
    router.push({ name: 'orders' })
  }
  catch {
    error.value = 'Неверный логин или пароль'
  }
  finally {
    loading.value = false
  }
}
</script>

<template>
  <v-main class="login">
    <v-card class="login__card" elevation="4">
      <h1 class="login__title font-display">🌱 Админка</h1>
      <p class="login__hint">Микрозелень — панель управления</p>
      <v-form @submit.prevent="submit">
        <v-text-field v-model="username" label="Логин" autofocus class="mb-1" />
        <v-text-field v-model="password" label="Пароль" type="password" class="mb-1" />
        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-4"
        >
          {{ error }}
        </v-alert>
        <v-btn type="submit" color="primary" block size="large" :loading="loading">
          Войти
        </v-btn>
      </v-form>
    </v-card>
  </v-main>
</template>

<style scoped>
.login {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.login__card {
  width: 100%;
  max-width: 380px;
  padding: 2rem;
}

.login__title {
  font-size: 1.7rem;
  font-weight: 600;
  color: var(--color-forest, #1f3d2b);
  margin: 0 0 0.25rem;
}

.login__hint {
  font-size: 0.9rem;
  opacity: 0.7;
  margin: 0 0 1.5rem;
}
</style>
