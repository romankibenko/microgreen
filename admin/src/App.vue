<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

function logout(): void {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <v-app>
    <router-view v-if="route.meta.public" />

    <template v-else>
      <v-app-bar flat color="primary" density="comfortable">
        <v-app-bar-title class="font-display">🌱 Микрозелень — админка</v-app-bar-title>
        <v-btn variant="text" :to="{ name: 'orders' }">Заказы</v-btn>
        <v-btn variant="text" :to="{ name: 'products' }">Товары</v-btn>
        <v-btn variant="text" :to="{ name: 'plantings' }">Посадки</v-btn>
        <v-btn variant="text" prepend-icon="mdi-logout" @click="logout">Выйти</v-btn>
      </v-app-bar>

      <v-main>
        <v-container class="py-8">
          <router-view />
        </v-container>
      </v-main>
    </template>
  </v-app>
</template>
