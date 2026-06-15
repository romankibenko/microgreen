<script setup lang="ts">
import type { Product } from '@/api/types'
import { cultureGradient, formatPrice, pluralLotki } from '@/utils/format'

interface Props {
  product: Product | null
}

interface Emits {
  add: [product: Product]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const open = defineModel<boolean>({ default: false })

function addToCart(): void {
  if (props.product) emit('add', props.product)
  open.value = false
}
</script>

<template>
  <v-dialog v-model="open" max-width="560" content-class="detail-dialog">
    <v-card v-if="product" class="detail">
      <div class="detail__media">
        <v-img
          v-if="product.image_url"
          :src="product.image_url"
          :alt="product.name"
          cover
          height="260"
        />
        <div
          v-else
          class="detail__placeholder"
          :style="{ background: cultureGradient(product.name) }"
        >
          🌱
        </div>
        <v-btn
          class="detail__close"
          icon="mdi-close"
          variant="flat"
          size="small"
          aria-label="Закрыть"
          @click="open = false"
        />
      </div>

      <div class="detail__body">
        <h2 class="detail__name font-display">{{ product.name }}</h2>

        <p
          class="detail__stock"
          :class="{ 'detail__stock--out': product.stock <= 0 }"
        >
          {{ product.stock > 0
            ? `🟢 готово к продаже: ${product.stock} ${pluralLotki(product.stock)}`
            : '⚪ нет в наличии' }}
        </p>

        <p v-if="product.description" class="detail__desc">
          {{ product.description }}
        </p>
        <p v-else class="detail__desc detail__desc--empty">
          Описание скоро появится.
        </p>

        <div class="detail__footer">
          <div class="detail__price">
            <span class="detail__amount">{{ formatPrice(product.price) }}</span>
            <span v-if="product.unit" class="detail__unit">/ {{ product.unit }}</span>
          </div>
          <v-btn
            color="primary"
            variant="flat"
            size="large"
            prepend-icon="mdi-cart-plus"
            :disabled="product.stock <= 0"
            @click="addToCart"
          >
            В корзину
          </v-btn>
        </div>
      </div>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.detail {
  overflow: hidden;
}

.detail__media {
  position: relative;
}

.detail__placeholder {
  height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5rem;
}

.detail__close {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: rgba(255, 255, 255, 0.85);
}

.detail__body {
  padding: 1.5rem;
}

.detail__name {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0 0 0.5rem;
}

.detail__stock {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0 0 1rem;
}

.detail__stock--out {
  color: var(--color-ink);
  opacity: 0.55;
  font-weight: 500;
}

.detail__desc {
  font-size: 0.98rem;
  line-height: 1.6;
  color: var(--color-ink);
  opacity: 0.82;
  white-space: pre-line;
  margin: 0 0 1.5rem;
}

.detail__desc--empty {
  font-style: italic;
  opacity: 0.55;
}

.detail__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.detail__amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-forest);
}

.detail__unit {
  font-size: 0.9rem;
  color: var(--color-ink);
  opacity: 0.6;
  margin-left: 0.35rem;
}
</style>

<!-- Блюр фона лендинга под модалкой (scrim вынесен из scope, поэтому глобально) -->
<style>
.v-overlay:has(.detail-dialog) .v-overlay__scrim {
  backdrop-filter: blur(6px);
  opacity: 0.45;
}
</style>
