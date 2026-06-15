<script setup lang="ts">
import type { Product } from '@/api/types'
import { useProducts } from '@/composables/useProducts'

import ProductCard from './ProductCard.vue'

interface Emits {
  add: [product: Product]
  details: [product: Product]
}

const emit = defineEmits<Emits>()

const { products, loading, error, load } = useProducts()
</script>

<template>
  <section id="catalog" class="catalog">
    <header class="catalog__head">
      <h2 class="catalog__title font-display">Что растёт прямо сейчас</h2>
      <p class="catalog__subtitle">Выбирайте — соберём заказ и принесём свежим.</p>
    </header>

    <div v-if="loading" class="catalog__state">
      <v-progress-circular indeterminate color="primary" size="40" />
    </div>

    <div v-else-if="error" class="catalog__state">
      <p class="catalog__error">{{ error }}</p>
      <v-btn color="primary" variant="tonal" @click="load">Повторить</v-btn>
    </div>

    <p v-else-if="products.length === 0" class="catalog__state">
      Каталог пока пуст — заглядывайте чуть позже.
    </p>

    <div v-else class="catalog__grid">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        @add="emit('add', $event)"
        @details="emit('details', $event)"
      />
    </div>
  </section>
</template>

<style scoped>
.catalog {
  max-width: 1120px;
  margin: 0 auto;
  padding: clamp(2rem, 5vw, 4rem) 1.25rem 5rem;
}

.catalog__head {
  margin-bottom: 2rem;
}

.catalog__title {
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 600;
  color: var(--color-forest);
  margin: 0 0 0.5rem;
}

.catalog__subtitle {
  font-size: 1.05rem;
  color: var(--color-ink);
  opacity: 0.7;
  margin: 0;
}

.catalog__state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 0;
  text-align: center;
}

.catalog__error {
  color: #9a3a2a;
  margin: 0;
}

.catalog__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 270px), 1fr));
  gap: 1.5rem;
}
</style>
