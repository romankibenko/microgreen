<script setup lang="ts">
import { ref } from 'vue'

import { createOrder } from '@/api/client'
import type { Order } from '@/api/types'
import { useCartStore } from '@/stores/cart'
import { formatPrice } from '@/utils/format'

interface Emits {
  success: [order: Order]
}

const open = defineModel<boolean>({ default: false })
const emit = defineEmits<Emits>()

const cart = useCartStore()

const phone = ref('')
const name = ref('')
const comment = ref('')
const submitting = ref(false)
const errorMessage = ref<string | null>(null)

const phoneRules = [
  (v: string) => !!v.trim() || 'Укажите телефон для связи',
  (v: string) => v.trim().length >= 5 || 'Телефон слишком короткий',
]

async function submit(): Promise<void> {
  if (phone.value.trim().length < 5 || cart.isEmpty) return

  submitting.value = true
  errorMessage.value = null
  try {
    const order = await createOrder({
      customer_phone: phone.value.trim(),
      customer_name: name.value.trim() || null,
      comment: comment.value.trim() || null,
      items: cart.items.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity,
      })),
    })
    cart.clear()
    phone.value = ''
    name.value = ''
    comment.value = ''
    open.value = false
    emit('success', order)
  }
  catch {
    errorMessage.value = 'Не удалось оформить заказ. Проверьте данные и попробуйте ещё раз.'
  }
  finally {
    submitting.value = false
  }
}
</script>

<template>
  <v-dialog v-model="open" max-width="460">
    <v-card class="checkout">
      <h2 class="checkout__title font-display">Оформление заказа</h2>
      <p class="checkout__hint">
        Оставьте телефон — позвоним, согласуем время и принесём заказ к подъезду.
      </p>

      <v-form class="checkout__form" @submit.prevent="submit">
        <v-text-field
          v-model="phone"
          label="Телефон"
          type="tel"
          placeholder="+7 999 123-45-67"
          :rules="phoneRules"
          required
        />
        <v-text-field v-model="name" label="Имя (необязательно)" />
        <v-textarea
          v-model="comment"
          label="Комментарий (подъезд, этаж, время)"
          rows="2"
          auto-grow
        />

        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          density="compact"
          class="checkout__error"
        >
          {{ errorMessage }}
        </v-alert>

        <div class="checkout__total">
          <span>К оплате при получении</span>
          <span class="checkout__amount font-display">{{ formatPrice(cart.total) }}</span>
        </div>

        <v-btn
          type="submit"
          color="primary"
          size="large"
          variant="flat"
          block
          :loading="submitting"
          :disabled="cart.isEmpty"
        >
          Подтвердить заказ
        </v-btn>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.checkout {
  padding: 1.75rem;
}

.checkout__title {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0 0 0.4rem;
}

.checkout__hint {
  font-size: 0.92rem;
  color: var(--color-ink);
  opacity: 0.72;
  margin: 0 0 1.25rem;
}

.checkout__form {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.checkout__error {
  margin-bottom: 0.75rem;
}

.checkout__total {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin: 0.5rem 0 1.25rem;
  font-size: 1rem;
}

.checkout__amount {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-forest);
}
</style>
