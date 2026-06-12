<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { fetchOrders, setOrderStatus } from '@/api/client'
import type { Order, OrderStatus } from '@/api/types'

const orders = ref<Order[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const statusOptions: { value: OrderStatus; title: string }[] = [
  { value: 'new', title: '🆕 Новый' },
  { value: 'assembled', title: '📦 Собран' },
  { value: 'delivered', title: '✅ Доставлен' },
  { value: 'cancelled', title: '❌ Отменён' },
]

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    orders.value = await fetchOrders()
  }
  catch {
    error.value = 'Не удалось загрузить заказы'
  }
  finally {
    loading.value = false
  }
}

async function changeStatus(order: Order, status: OrderStatus): Promise<void> {
  const updated = await setOrderStatus(order.id, status)
  order.status = updated.status
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatPrice(value: string): string {
  return Number(value).toLocaleString('ru-RU')
}

onMounted(load)
</script>

<template>
  <div class="d-flex align-center mb-6">
    <h1 class="text-h5 font-display">Заказы</h1>
    <v-spacer />
    <v-btn variant="text" prepend-icon="mdi-refresh" :loading="loading" @click="load">
      Обновить
    </v-btn>
  </div>

  <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

  <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />

  <p v-else-if="orders.length === 0" class="text-medium-emphasis">
    Заказов пока нет.
  </p>

  <v-row v-else>
    <v-col v-for="order in orders" :key="order.id" cols="12" md="6">
      <v-card class="pa-4" elevation="2">
        <div class="d-flex align-center mb-2">
          <span class="text-subtitle-1 font-weight-bold">Заказ №{{ order.id }}</span>
          <v-spacer />
          <span class="text-caption text-medium-emphasis">
            {{ formatDate(order.created_at) }}
          </span>
        </div>

        <div class="text-body-2 mb-1">
          📞 {{ order.customer_phone }}
          <span v-if="order.customer_name">· {{ order.customer_name }}</span>
        </div>
        <div v-if="order.comment" class="text-body-2 text-medium-emphasis mb-2">
          💬 {{ order.comment }}
        </div>

        <v-divider class="my-2" />

        <div v-for="item in order.items" :key="item.id" class="text-body-2">
          {{ item.product_name }} × {{ item.quantity }}
        </div>

        <div class="text-subtitle-2 font-weight-bold mt-2 mb-3">
          Итого: {{ formatPrice(order.total) }} ₽
        </div>

        <v-select
          :model-value="order.status"
          :items="statusOptions"
          label="Статус"
          hide-details
          @update:model-value="changeStatus(order, $event)"
        />
      </v-card>
    </v-col>
  </v-row>
</template>
