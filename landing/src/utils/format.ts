const rubFormatter = new Intl.NumberFormat('ru-RU', {
  style: 'currency',
  currency: 'RUB',
  maximumFractionDigits: 0,
})

export function formatPrice(value: number | string): string {
  return rubFormatter.format(Number(value))
}

export function pluralLotki(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return 'лоток'
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return 'лотка'
  return 'лотков'
}

// Стабильный «ботанический» градиент по названию культуры — плейсхолдер под фото.
export function cultureGradient(name: string): string {
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = (hash * 31 + name.charCodeAt(i)) >>> 0
  const hue = 70 + (hash % 90) // 70–160°: от салатового до изумрудного
  return `linear-gradient(135deg, hsl(${hue} 42% 50%), hsl(${hue + 25} 48% 34%))`
}
