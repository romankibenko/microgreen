<script setup lang="ts">
import { onMounted, ref } from 'vue'

import {
  createProduct,
  deleteProduct,
  fetchProducts,
  updateProduct,
} from '@/api/client'
import type { Product, ProductPayload } from '@/api/types'

const products = ref<Product[]>([])
const loading = ref(true)
const listError = ref<string | null>(null)

const dialog = ref(false)
const editingId = ref<number | null>(null)
const saving = ref(false)
const formError = ref<string | null>(null)

const form = ref<ProductPayload>(blankForm())

function blankForm(): ProductPayload {
  return {
    name: '',
    description: null,
    price: '',
    unit: null,
    image_url: null,
    is_active: true,
    stock: 0,
  }
}

async function load(): Promise<void> {
  loading.value = true
  products.value = await fetchProducts()
  loading.value = false
}

function openCreate(): void {
  editingId.value = null
  form.value = blankForm()
  formError.value = null
  dialog.value = true
}

function openEdit(p: Product): void {
  editingId.value = p.id
  form.value = {
    name: p.name,
    description: p.description,
    price: p.price,
    unit: p.unit,
    image_url: p.image_url,
    is_active: p.is_active,
    stock: p.stock,
  }
  formError.value = null
  dialog.value = true
}

async function save(): Promise<void> {
  if (!form.value.name.trim() || form.value.price === '') {
    formError.value = 'Заполни название и цену'
    return
  }
  saving.value = true
  formError.value = null
  try {
    if (editingId.value === null) await createProduct(form.value)
    else await updateProduct(editingId.value, form.value)
    dialog.value = false
    await load()
  }
  catch {
    formError.value = 'Не удалось сохранить товар'
  }
  finally {
    saving.value = false
  }
}

async function remove(id: number): Promise<void> {
  listError.value = null
  try {
    await deleteProduct(id)
    await load()
  }
  catch {
    listError.value = 'Нельзя удалить: товар уже встречается в заказах. Снимите «Активен».'
  }
}

function formatPrice(p: string): string {
  return `${Number(p).toLocaleString('ru-RU')} ₽`
}

onMounted(load)
</script>

<template>
  <div class="d-flex align-center justify-space-between mb-6">
    <h1 class="text-h5 font-display">Товары</h1>
    <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreate">
      Добавить товар
    </v-btn>
  </div>

  <v-alert
    v-if="listError"
    type="error"
    variant="tonal"
    density="compact"
    closable
    class="mb-4"
    @click:close="listError = null"
  >
    {{ listError }}
  </v-alert>

  <v-progress-linear v-if="loading" indeterminate color="primary" />

  <p v-else-if="products.length === 0" class="text-medium-emphasis">
    Товаров пока нет — добавь первый.
  </p>

  <v-table v-else>
    <thead>
      <tr>
        <th>Фото</th>
        <th>Название</th>
        <th>Цена</th>
        <th>Ед.</th>
        <th>Наличие</th>
        <th>Активен</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <tr v-for="p in products" :key="p.id">
        <td>
          <v-avatar v-if="p.image_url" size="40" rounded>
            <v-img :src="p.image_url" :alt="p.name" cover />
          </v-avatar>
          <span v-else>🌱</span>
        </td>
        <td class="font-weight-medium">{{ p.name }}</td>
        <td>{{ formatPrice(p.price) }}</td>
        <td class="text-medium-emphasis">{{ p.unit || '—' }}</td>
        <td>
          <v-chip :color="p.stock > 0 ? 'secondary' : 'default'" size="small" variant="flat">
            {{ p.stock }}
          </v-chip>
        </td>
        <td>
          <v-icon :color="p.is_active ? 'success' : 'disabled'">
            {{ p.is_active ? 'mdi-check-circle' : 'mdi-circle-outline' }}
          </v-icon>
        </td>
        <td class="text-no-wrap">
          <v-btn
            icon="mdi-pencil-outline"
            variant="text"
            size="small"
            @click="openEdit(p)"
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

  <v-dialog v-model="dialog" max-width="520">
    <v-card>
      <v-card-title class="font-display">
        {{ editingId === null ? 'Новый товар' : 'Редактирование товара' }}
      </v-card-title>
      <v-card-text>
        <v-text-field v-model="form.name" label="Название" class="mb-2" hide-details />
        <v-textarea
          v-model="form.description"
          label="Описание"
          rows="2"
          auto-grow
          class="mb-2"
          hide-details
        />
        <v-row dense>
          <v-col cols="6">
            <v-text-field
              v-model="form.price"
              label="Цена, ₽"
              type="number"
              min="0"
              hide-details
            />
          </v-col>
          <v-col cols="6">
            <v-text-field v-model="form.unit" label="Единица" hide-details />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model.number="form.stock"
              label="Наличие (лотков)"
              type="number"
              min="0"
              hide-details
            />
          </v-col>
          <v-col cols="6" class="d-flex align-center">
            <v-switch
              v-model="form.is_active"
              label="Активен"
              color="primary"
              hide-details
            />
          </v-col>
        </v-row>
        <v-text-field
          v-model="form.image_url"
          label="URL фото"
          class="mt-2"
          hide-details
        />
        <v-alert
          v-if="formError"
          type="error"
          variant="tonal"
          density="compact"
          class="mt-3"
        >
          {{ formError }}
        </v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
        <v-btn color="primary" variant="flat" :loading="saving" @click="save">
          Сохранить
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
