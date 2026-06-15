<script setup lang="ts">
import type { Product } from '@/api/types'
import { formatPrice } from '@/utils/format'

interface Props {
  product: Product
}

interface Emits {
  add: [product: Product]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
</script>

<template>
  <v-card class="product-card" elevation="0" border>
    <div class="product-card__media">
      <v-img
        v-if="props.product.image_url"
        :src="props.product.image_url"
        :alt="props.product.name"
        cover
        height="220"
      />
      <div v-else class="product-card__placeholder">🌱</div>
    </div>

    <div class="product-card__body">
      <h3 class="product-card__name font-display">
        {{ props.product.name }}
      </h3>
      <p v-if="props.product.description" class="product-card__desc">
        {{ props.product.description }}
      </p>

      <p
        class="product-card__stock"
        :class="{ 'product-card__stock--out': props.product.stock <= 0 }"
      >
        {{ props.product.stock > 0
          ? `🟢 готово к продаже: ${props.product.stock}`
          : '⚪ нет в наличии' }}
      </p>

      <div class="product-card__footer">
        <div class="product-card__price">
          <span class="product-card__amount">{{ formatPrice(props.product.price) }}</span>
          <span v-if="props.product.unit" class="product-card__unit">
            / {{ props.product.unit }}
          </span>
        </div>
        <v-btn
          color="primary"
          variant="flat"
          icon="mdi-plus"
          size="small"
          :disabled="props.product.stock <= 0"
          :aria-label="`Добавить «${props.product.name}» в корзину`"
          @click="emit('add', props.product)"
        />
      </div>
    </div>
  </v-card>
</template>

<style scoped>
.product-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--color-cream);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 40px -24px rgba(31, 61, 43, 0.55);
}

.product-card__media {
  background: #e9ecdf;
}

.product-card__placeholder {
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  opacity: 0.5;
}

.product-card__body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1.1rem 1.2rem 1.2rem;
  flex: 1;
}

.product-card__name {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0;
}

.product-card__desc {
  font-size: 0.92rem;
  line-height: 1.45;
  color: var(--color-ink);
  opacity: 0.72;
  margin: 0;
}

.product-card__stock {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0;
}

.product-card__stock--out {
  color: var(--color-ink);
  opacity: 0.55;
  font-weight: 500;
}

.product-card__footer {
  margin-top: auto;
  padding-top: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-card__amount {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-forest);
}

.product-card__unit {
  font-size: 0.85rem;
  color: var(--color-ink);
  opacity: 0.6;
}
</style>
