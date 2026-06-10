<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { formatPrice } from '@/utils/format'

import CartItemRow from './CartItemRow.vue'

interface Emits {
  checkout: []
}

const open = defineModel<boolean>({ default: false })
const emit = defineEmits<Emits>()

const cart = useCartStore()
</script>

<template>
  <v-navigation-drawer
    v-model="open"
    location="right"
    temporary
    width="400"
  >
    <div class="cart">
      <div class="cart__head">
        <h2 class="cart__title font-display">Корзина</h2>
        <v-btn icon="mdi-close" variant="text" aria-label="Закрыть" @click="open = false" />
      </div>

      <p v-if="cart.isEmpty" class="cart__empty">
        Здесь пока пусто. Добавьте зелень из каталога 🌱
      </p>

      <template v-else>
        <div class="cart__items">
          <CartItemRow
            v-for="item in cart.items"
            :key="item.product.id"
            :item="item"
            @update-quantity="cart.setQuantity"
            @remove="cart.remove"
          />
        </div>

        <div class="cart__footer">
          <div class="cart__total">
            <span>Итого</span>
            <span class="cart__total-amount font-display">{{ formatPrice(cart.total) }}</span>
          </div>
          <v-btn
            color="primary"
            size="large"
            variant="flat"
            block
            @click="emit('checkout')"
          >
            Оформить заказ
          </v-btn>
        </div>
      </template>
    </div>
  </v-navigation-drawer>
</template>

<style scoped>
.cart {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 1.25rem;
}

.cart__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.cart__title {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0;
}

.cart__empty {
  margin-top: 2rem;
  text-align: center;
  color: var(--color-ink);
  opacity: 0.7;
}

.cart__items {
  flex: 1;
  overflow-y: auto;
}

.cart__footer {
  padding-top: 1rem;
}

.cart__total {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 1.05rem;
}

.cart__total-amount {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--color-forest);
}
</style>
