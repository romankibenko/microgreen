<script setup lang="ts">
import type { CartItem } from '@/stores/cart'
import { formatPrice } from '@/utils/format'

interface Props {
  item: CartItem
}

interface Emits {
  updateQuantity: [productId: number, quantity: number]
  remove: [productId: number]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

function changeBy(delta: number): void {
  emit('updateQuantity', props.item.product.id, props.item.quantity + delta)
}
</script>

<template>
  <div class="cart-row">
    <div class="cart-row__info">
      <span class="cart-row__name">{{ props.item.product.name }}</span>
      <span class="cart-row__price">
        {{ formatPrice(props.item.product.price) }}
        <template v-if="props.item.product.unit">/ {{ props.item.product.unit }}</template>
      </span>
    </div>

    <div class="cart-row__qty">
      <v-btn
        icon="mdi-minus"
        size="x-small"
        variant="tonal"
        aria-label="Уменьшить количество"
        @click="changeBy(-1)"
      />
      <span class="cart-row__count">{{ props.item.quantity }}</span>
      <v-btn
        icon="mdi-plus"
        size="x-small"
        variant="tonal"
        aria-label="Увеличить количество"
        @click="changeBy(1)"
      />
    </div>

    <v-btn
      icon="mdi-close"
      size="x-small"
      variant="text"
      aria-label="Убрать из корзины"
      @click="emit('remove', props.item.product.id)"
    />
  </div>
</template>

<style scoped>
.cart-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(31, 61, 43, 0.1);
}

.cart-row__info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  flex: 1;
  min-width: 0;
}

.cart-row__name {
  font-weight: 600;
  color: var(--color-forest);
}

.cart-row__price {
  font-size: 0.82rem;
  color: var(--color-ink);
  opacity: 0.65;
}

.cart-row__qty {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cart-row__count {
  min-width: 1.5rem;
  text-align: center;
  font-weight: 600;
}
</style>
