# 🌱 Микрозелень — платформа локального производства и продажи

Гиперлокальный сервис по выращиванию и доставке свежей микрозелени с полной IT-автоматизацией: публичный лендинг с заказами, Telegram-бот, закрытая админ-панель и единое REST API.

> **Pet-проект полного цикла:** от модели данных до деплоя в прод. Один продукт собирает весь стек — backend, frontend, бота, инфраструктуру.

![Status](https://img.shields.io/badge/status-in_development-orange)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

---

## Что умеет

- 🛒 **Лендинг с каталогом и корзиной** — заказ оформляется в пару кликов, гостевой (по телефону, без регистрации).
- 🤖 **Telegram-бот** — мгновенные уведомления о заказах, каталог и статусы прямо в чате.
- 📊 **Админ-панель** — управление заказами, журнал посадок с авторасчётом даты готовности урожая.
- 🔌 **Единое REST API** — один backend обслуживает все три клиента.

## Архитектура

```
                    ┌──────────────┐
   Лендинг (Vue 3) ─┤              │
   Бот (aiogram 3) ─┤  REST API    ├─ PostgreSQL
   Админка (Vue 3) ─┤  (FastAPI)   │
                    └──────────────┘
        всё в Docker Compose за Nginx (HTTPS)
```

## Стек

| Слой | Технологии |
|------|-----------|
| **Backend** | Python 3.12, FastAPI, Pydantic v2, asyncpg, Alembic, JWT |
| **База данных** | PostgreSQL |
| **Лендинг / Админка** | Vue 3, Vuetify, Pinia |
| **Бот** | aiogram 3 |
| **Инфраструктура** | Docker Compose, Nginx, Let's Encrypt, VDS |

## Структура репозитория

```
microgreen/
├── backend/    # FastAPI + PostgreSQL + Alembic
├── landing/    # Vue 3 — публичный сайт
├── admin/      # Vue 3 — закрытая панель (JWT)
├── bot/        # aiogram 3 — Telegram-бот
└── docker-compose.yml
```

## Дорожная карта

- [x] **Этап 0** — скелет монорепо, Docker Compose, healthcheck
- [x] **Этап 1** — backend-ядро: товары, заказы, журнал посадок
- [x] **Этап 2** — лендинг: каталог, корзина, оформление заказа
- [x] **Этап 3** — Telegram-бот: уведомления о заказах, каталог, статусы
- [x] **Этап 4** — админ-панель: заказы, статусы, посадки
- [ ] **Этап 5** — деплой в прод: домен, HTTPS, мониторинг
- [ ] **После MVP** — онлайн-оплата (ЮKassa), LLM-консультант, аналитика

## Запуск (локально)

```bash
cp .env.example .env   # заполнить переменные
docker compose up --build
```

API будет доступно на `http://localhost:8000`, документация — на `/docs`.

---

<sub>Разработка: Роман Кибенко · backend-разработчик, Python / Vue / Telegram-боты</sub>
