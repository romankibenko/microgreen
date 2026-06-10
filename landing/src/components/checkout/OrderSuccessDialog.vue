<script setup lang="ts">
import type { Order } from '@/api/types'
import { BOT_URL } from '@/config'

interface Props {
  order: Order | null
}

defineProps<Props>()
const open = defineModel<boolean>({ default: false })
</script>

<template>
  <v-dialog v-model="open" max-width="420">
    <v-card v-if="order" class="success">
      <div class="success__mark">✅</div>
      <h2 class="success__title font-display">Заказ №{{ order.id }} принят!</h2>
      <p class="success__text">
        Скоро позвоним, согласуем время и принесём заказ к подъезду 🌱
      </p>

      <template v-if="BOT_URL">
        <p class="success__hint">Хочешь видеть статус заказа?</p>
        <v-btn
          :href="BOT_URL"
          target="_blank"
          rel="noopener"
          color="primary"
          size="large"
          variant="flat"
          block
          prepend-icon="mdi-send"
        >
          Открыть Telegram-бот
        </v-btn>
        <p class="success__note">
          Подпишись тем же номером — пришлём статусы заказа.
        </p>
      </template>

      <v-btn
        v-else
        color="primary"
        variant="flat"
        block
        @click="open = false"
      >
        Отлично
      </v-btn>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.success {
  padding: 2rem 1.75rem 1.75rem;
  text-align: center;
}

.success__mark {
  font-size: 2.75rem;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.success__title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0 0 0.5rem;
}

.success__text {
  font-size: 0.95rem;
  color: var(--color-ink);
  opacity: 0.78;
  margin: 0 0 1.5rem;
}

.success__hint {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0 0 0.75rem;
}

.success__note {
  font-size: 0.82rem;
  color: var(--color-ink);
  opacity: 0.66;
  margin: 0.75rem 0 0;
}
</style>
