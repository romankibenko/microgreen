<script setup lang="ts">
import { computed, ref } from 'vue'

import cropsData from '@/data/crops.json'

interface Crop {
  name: string
  grown: boolean
  description: string
  soak: string
  substrate: string
  density: string
  press: string
  germination: string
  height: string
  yield: string
  growth: string
  note: string
}

// Справочник агротехники — статичные данные из «Норм посева от Зелёного Шефа».
const crops = cropsData as Crop[]

// Пары «поле → человекочитаемый лейбл» для таблицы параметров карточки.
const params: { key: keyof Crop; label: string }[] = [
  { key: 'soak', label: 'Замачивание' },
  { key: 'substrate', label: 'На чём растить' },
  { key: 'density', label: 'Плотность посева' },
  { key: 'press', label: 'Прижим' },
  { key: 'germination', label: 'Прорастание (20–22 °C)' },
  { key: 'height', label: 'Высота на финише' },
  { key: 'yield', label: 'Урожайность (семена/зелень)' },
  { key: 'growth', label: 'Рост после прорастания' },
  { key: 'note', label: 'Важный нюанс' },
]

const search = ref('')
const onlyGrown = ref(false)

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  return crops.filter((c) => {
    if (onlyGrown.value && !c.grown) return false
    return q === '' || c.name.toLowerCase().includes(q)
  })
})
</script>

<template>
  <div class="d-flex align-center flex-wrap mb-2">
    <h1 class="text-h5 font-display">Справочник культур</h1>
    <v-spacer />
    <span class="text-caption text-medium-emphasis">
      Нормы посева от Зелёного Шефа · {{ crops.length }} культур
    </span>
  </div>

  <div class="d-flex align-center flex-wrap ga-4 mb-6">
    <v-text-field
      v-model="search"
      placeholder="Поиск по названию…"
      prepend-inner-icon="mdi-magnify"
      density="compact"
      variant="outlined"
      hide-details
      clearable
      style="max-width: 340px"
    />
    <v-switch
      v-model="onlyGrown"
      label="Только те, что растим"
      color="primary"
      density="compact"
      hide-details
    />
  </div>

  <p v-if="filtered.length === 0" class="text-medium-emphasis">
    Ничего не найдено.
  </p>

  <v-row v-else>
    <v-col v-for="crop in filtered" :key="crop.name" cols="12" md="6" lg="4">
      <v-card class="pa-4 h-100" elevation="2">
        <div class="d-flex align-center mb-1">
          <h3 class="text-subtitle-1 font-weight-bold">{{ crop.name }}</h3>
          <v-spacer />
          <v-chip v-if="crop.grown" color="secondary" size="x-small" variant="flat">
            🌿 растим
          </v-chip>
        </div>

        <p class="text-body-2 text-medium-emphasis mb-3">{{ crop.description }}</p>

        <v-divider class="mb-2" />

        <div v-for="p in params" :key="p.key" class="d-flex text-body-2 py-1">
          <span class="text-medium-emphasis param-label">{{ p.label }}</span>
          <span class="param-value">{{ crop[p.key] }}</span>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped>
.param-label {
  flex: 0 0 46%;
}

.param-value {
  flex: 1 1 auto;
  font-weight: 500;
}
</style>
