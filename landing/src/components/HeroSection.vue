<script setup lang="ts">
interface Emits {
  browse: []
}

const emit = defineEmits<Emits>()
</script>

<template>
  <section id="top" class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">Срезаем в день заказа · доставка по соседям</p>
      <h1 class="hero__title font-display text-balance">
        Микрозелень,<br >выросшая <em>в двух шагах</em> от вашей двери
      </h1>
      <p class="hero__lead text-balance">
        Никаких складов и перекупов. Сеем, растим и приносим живые ростки прямо
        к подъезду — свежие, хрустящие, полные вкуса.
      </p>
      <v-btn
        color="primary"
        size="x-large"
        variant="flat"
        append-icon="mdi-arrow-down"
        @click="emit('browse')"
      >
        Смотреть каталог
      </v-btn>
    </div>
    <div class="hero__leaf" aria-hidden="true">🌿</div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  max-width: 1120px;
  margin: 0 auto;
  padding: clamp(3rem, 8vw, 6rem) 1.25rem clamp(2rem, 5vw, 4rem);
  overflow: hidden;
}

.hero__content {
  position: relative;
  z-index: 2;
  max-width: 680px;
}

.hero__eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-forest);
  opacity: 0.7;
  margin: 0 0 1.25rem;
}

.hero__title {
  font-size: clamp(2.4rem, 6vw, 4.2rem);
  line-height: 1.02;
  font-weight: 600;
  color: var(--color-forest);
  margin: 0 0 1.5rem;
}

.hero__title em {
  font-style: italic;
  color: #4a7c2f;
}

.hero__lead {
  font-size: clamp(1rem, 2vw, 1.2rem);
  line-height: 1.55;
  color: var(--color-ink);
  opacity: 0.82;
  max-width: 520px;
  margin: 0 0 2rem;
}

.hero__leaf {
  position: absolute;
  right: -2rem;
  bottom: -3rem;
  font-size: clamp(10rem, 30vw, 22rem);
  line-height: 1;
  opacity: 0.12;
  z-index: 1;
  transform: rotate(-12deg);
  user-select: none;
}
</style>
