<script setup lang="ts">
import { onMounted, ref } from 'vue'

import {
  createPlanting,
  deletePlanting,
  fetchPlantings,
  updatePlantingNote,
} from '@/api/client'
import type { Planting, PlantingStage } from '@/api/types'
import { CULTURES } from '@/config'

const plantings = ref<Planting[]>([])
const loading = ref(true)

const culture = ref<string | null>(null)
const sownAt = ref(new Date().toISOString().slice(0, 10))
const growDays = ref<number | null>(null)
const shadeDays = ref<number>(3)
const trays = ref<number>(1)
const note = ref('')
const saving = ref(false)
const formError = ref<string | null>(null)

const editingId = ref<number | null>(null)
const editNoteText = ref('')

const STAGE_LABEL: Record<PlantingStage, string> = {
  shade: 'в тени',
  light: 'на свету',
  ready: 'готово',
}
const STAGE_COLOR: Record<PlantingStage, string> = {
  shade: 'blue-grey',
  light: 'amber-darken-2',
  ready: 'accent',
}

async function load(): Promise<void> {
  loading.value = true
  plantings.value = await fetchPlantings()
  loading.value = false
}

async function add(): Promise<void> {
  if (!culture.value || !growDays.value || !trays.value) {
    formError.value = 'Заполни культуру, дни роста и количество лотков'
    return
  }
  if (shadeDays.value > growDays.value) {
    formError.value = 'Дней в тени не может быть больше дней роста'
    return
  }
  saving.value = true
  formError.value = null
  try {
    await createPlanting({
      culture: culture.value,
      sown_at: sownAt.value,
      grow_days: growDays.value,
      shade_days: shadeDays.value,
      trays: trays.value,
      note: note.value.trim() || null,
    })
    culture.value = null
    growDays.value = null
    shadeDays.value = 3
    trays.value = 1
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

function startEdit(p: Planting): void {
  editingId.value = p.id
  editNoteText.value = p.note ?? ''
}

function cancelEdit(): void {
  editingId.value = null
}

async function saveEdit(id: number): Promise<void> {
  await updatePlantingNote(id, editNoteText.value.trim() || null)
  editingId.value = null
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
        <v-select
          v-model="culture"
          :items="CULTURES"
          label="Культура"
          hide-details
        />
      </v-col>
      <v-col cols="6" sm="4">
        <v-text-field v-model="sownAt" label="Дата посева" type="date" hide-details />
      </v-col>
      <v-col cols="6" sm="4">
        <v-text-field v-model="note" label="Заметка" hide-details />
      </v-col>
      <v-col cols="4" sm="4">
        <v-text-field
          v-model.number="growDays"
          label="Дней роста"
          type="number"
          min="1"
          hide-details
        />
      </v-col>
      <v-col cols="4" sm="4">
        <v-text-field
          v-model.number="shadeDays"
          label="Дней в тени"
          type="number"
          min="0"
          hide-details
        />
      </v-col>
      <v-col cols="4" sm="4">
        <v-text-field
          v-model.number="trays"
          label="Лотков"
          type="number"
          min="1"
          hide-details
        />
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
        <th>Лотков</th>
        <th>Этап</th>
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
        <td>{{ p.trays }}</td>
        <td>
          <v-chip :color="STAGE_COLOR[p.stage]" size="small" variant="flat">
            {{ STAGE_LABEL[p.stage] }}
          </v-chip>
        </td>
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
        <td class="text-medium-emphasis">
          <div v-if="editingId === p.id" class="d-flex align-center ga-1">
            <v-text-field
              v-model="editNoteText"
              density="compact"
              hide-details
              autofocus
              style="min-width: 140px"
              @keyup.enter="saveEdit(p.id)"
              @keyup.esc="cancelEdit"
            />
            <v-btn
              icon="mdi-check"
              variant="text"
              size="small"
              color="success"
              @click="saveEdit(p.id)"
            />
            <v-btn icon="mdi-close" variant="text" size="small" @click="cancelEdit" />
          </div>
          <span v-else>{{ p.note || '—' }}</span>
        </td>
        <td>
          <v-btn
            icon="mdi-pencil-outline"
            variant="text"
            size="small"
            @click="startEdit(p)"
          />
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
