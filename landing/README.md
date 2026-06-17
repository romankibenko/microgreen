# Лендинг — «Зелёный двор»

Публичный сайт на **Vue 3 + Vuetify 3 + Pinia** (Composition API, `<script setup lang="ts">`):
каталог из API, корзина, гостевое оформление заказа.

## Запуск (dev)

Нужен поднятый backend (см. корневой `README.md` → `docker compose up`).

```bash
npm install
npm run dev          # http://localhost:5173
```

API по умолчанию берётся с `http://localhost:8000`. Переопределить — переменной
`VITE_API_URL` (например в `.env`).

## Сборка

```bash
npm run build        # type-check (vue-tsc) + прод-сборка в dist/
```

## Структура

```
src/
  api/          # axios-клиент + типы
  components/   # AppHeader, HeroSection, catalog/, cart/, checkout/
  composables/  # useProducts — загрузка каталога
  stores/       # cart — корзина (Pinia)
  utils/        # format — цены в рублях
  plugins/      # vuetify — ботаническая тема
```
