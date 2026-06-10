<script setup lang="ts">
import { BOT_URL } from '@/config'

interface Props {
  cartCount: number
}

interface Emits {
  openCart: []
}

defineProps<Props>()
const emit = defineEmits<Emits>()
</script>

<template>
  <header class="site-header">
    <div class="site-header__inner">
      <a class="brand" href="#top">
        <span class="brand__mark">🌱</span>
        <span class="brand__name font-display">Зелёный двор</span>
      </a>

      <div class="site-header__actions">
        <v-btn
          v-if="BOT_URL"
          :href="BOT_URL"
          target="_blank"
          rel="noopener"
          variant="tonal"
          color="primary"
          icon="mdi-telegram"
          aria-label="Telegram-бот"
        />

        <v-btn
          color="primary"
          variant="flat"
          prepend-icon="mdi-basket-outline"
          @click="emit('openCart')"
        >
          Корзина
          <v-badge
            v-if="cartCount > 0"
            :content="cartCount"
            color="accent"
            text-color="primary"
            inline
          />
        </v-btn>
      </div>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(8px);
  background: rgba(246, 243, 234, 0.82);
  border-bottom: 1px solid rgba(31, 61, 43, 0.1);
}

.site-header__inner {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0.75rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  text-decoration: none;
  color: var(--color-forest);
}

.brand__mark {
  font-size: 1.5rem;
}

.brand__name {
  font-size: 1.4rem;
  font-weight: 600;
}

.site-header__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
