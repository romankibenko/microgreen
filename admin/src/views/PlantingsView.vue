<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { createPlanting, deletePlanting, fetchPlantings } from '@/api/client'
import type { Planting } from '@/api/types'

const plantings = ref<Planting[]>([])
const loading = ref(true)

const culture = ref('')
const sownAt = ref(new Date().toISOString().slice(0, 10))
const growDays = ref<number | null>(null)
const note = ref('')
const saving = ref(false)
const formError = ref<string | null>(null)

async function load(): Promise<void> {
  loading.value = true
  plantings.value = await fetchPlantings()
  loading.value = false
}

async function add(): Promise<void> {
  if (!culture.value.trim() || !growDays.value) {
    formError.value = 'Заполни культуру и количество дней роста'
    return
  }
  saving.value = true
  formError.value = null
  try {
    await createPlanting({
      culture: culture.value.trim(),
      sown_at: sownAt.value,
      grow_days: growDays.value,
      note: note.value.trim() || null,
    })
    culture.value = ''
    growDays.value = null
    note.value = ''
    await load()
  }
  catch {
    formError.value = 'Не удалось сохранить посадку'
  }
  finally {
    saving.value = false
  }
}

async function remove(id: number): Promise<void> {
  await deletePlanting(id)
  await load()
}

function formatDate(d: string): string {
  return new Date(d).toLocaleDateString('ru-RU')
}

function daysLeft(readyAt: string): number {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const ready = new Date(readyAt)
  return Math.round((ready.getTime() - today.getTime()) / 86_400_000)
}

onMounted(load)
</script>

<template>
  <h1 class="text-h5 font-display mb-6">Журнал посадок</h1>

  <v-card class="pa-4 mb-6" elevation="2">
    <div class="text-subtitle-2 mb-3">Новая посадка</div>
    <v-row dense>
      <v-col cols="12" sm="4">
        <v-text-field v-model="culture" label="Культура" hide-details />
      </v-col>
      <v-col cols="6" sm="3">
        <v-text-field v-model="sownAt" label="Дата посева" type="date" hide-details />
      </v-col>
      <v-col cols="6" sm="2">
        <v-text-field
          v-model.number="growDays"
          label="Дней роста"
          type="number"
          min="1"
          hide-details
        />
      </v-col>
      <v-col cols="12" sm="3">
        <v-text-field v-model="note" label="Заметка" hide-details />
      </v-col>
    </v-row>
    <v-alert
      v-if="formError"
      type="error"
      variant="tonal"
      density="compact"
      class="mt-3"
    >
      {{ formError }}
    </v-alert>
    <v-btn
      color="primary"
      class="mt-4"
      prepend-icon="mdi-sprout"
      :loading="saving"
      @click="add"
    >
      Добавить посадку
    </v-btn>
  </v-card>

  <v-progress-linear v-if="loading" indeterminate color="primary" />

  <p v-else-if="plantings.length === 0" class="text-medium-emphasis">
    Посадок пока нет — добавь первую сверху.
  </p>

  <v-table v-else>
    <thead>
      <tr>
        <th>Культура</th>
        <th>Посеяно</th>
        <th>Дней</th>
        <th>Готово</th>
        <th>Осталось</th>
        <th>Заметка</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr v-for="p in plantings" :key="p.id">
        <td class="font-weight-medium">{{ p.culture }}</td>
        <td>{{ formatDate(p.sown_at) }}</td>
        <td>{{ p.grow_days }}</td>
        <td>{{ formatDate(p.ready_at) }}</td>
        <td>
          <v-chip
            :color="daysLeft(p.ready_at) <= 0 ? 'accent' : 'secondary'"
            size="small"
            variant="flat"
          >
            {{ daysLeft(p.ready_at) <= 0 ? 'срезать!' : `${daysLeft(p.ready_at)} дн.` }}
          </v-chip>
        </td>
        <td class="text-medium-emphasis">{{ p.note || '—' }}</td>
        <td>
          <v-btn
            icon="mdi-delete-outline"
            variant="text"
            size="small"
            color="error"
            @click="remove(p.id)"
          />
        </td>
      </tr>
    </tbody>
  </v-table>
</template>
