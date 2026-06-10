import { onMounted, ref } from 'vue'

import { fetchProducts } from '@/api/client'
import type { Product } from '@/api/types'

export function useProducts() {
  const products = ref<Product[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function load(): Promise<void> {
    loading.value = true
    error.value = null
    try {
      products.value = await fetchProducts()
    }
    catch {
      error.value = 'Не удалось загрузить каталог. Попробуйте обновить страницу.'
    }
    finally {
      loading.value = false
    }
  }

  onMounted(load)

  return { products, loading, error, load }
}
