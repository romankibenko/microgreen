import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import type { Product } from '@/api/types'

export interface CartItem {
  product: Product
  quantity: number
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

  const count = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0),
  )

  const total = computed(() =>
    items.value.reduce(
      (sum, item) => sum + Number(item.product.price) * item.quantity,
      0,
    ),
  )

  const isEmpty = computed(() => items.value.length === 0)

  function add(product: Product, quantity = 1): void {
    const existing = items.value.find(item => item.product.id === product.id)
    if (existing) {
      existing.quantity += quantity
      return
    }
    items.value.push({ product, quantity })
  }

  function setQuantity(productId: number, quantity: number): void {
    const item = items.value.find(entry => entry.product.id === productId)
    if (!item) return
    if (quantity <= 0) {
      remove(productId)
      return
    }
    item.quantity = quantity
  }

  function remove(productId: number): void {
    items.value = items.value.filter(item => item.product.id !== productId)
  }

  function clear(): void {
    items.value = []
  }

  return { items, count, total, isEmpty, add, setQuantity, remove, clear }
})
