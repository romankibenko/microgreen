export const API_URL: string =
  import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

// Ключ JWT в localStorage.
export const TOKEN_KEY = 'admin_token'

// Фиксированный список культур для селектора в журнале посадок.
export const CULTURES: string[] = [
  'Лук шнитт',
  'Брокколи Калабрезе',
  'Капуста красная',
  'Мизуна красная',
  'Мизуна зелёная',
  'Редис Чайна Роуз',
  'Редис Санго',
  'Горох Мадрас',
  'Кинза',
  'Подсолнечник',
  'Горчица белая',
]
