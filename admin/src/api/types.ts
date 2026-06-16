export type OrderStatus = 'new' | 'assembled' | 'delivered' | 'cancelled'

export interface OrderItem {
  id: number
  product_id: number
  product_name: string
  unit_price: string
  quantity: number
}

export interface Order {
  id: number
  customer_phone: string
  customer_name: string | null
  comment: string | null
  status: OrderStatus
  total: string
  created_at: string
  items: OrderItem[]
}

export interface Product {
  id: number
  name: string
  description: string | null
  price: string
  unit: string | null
  image_url: string | null
  is_active: boolean
  sort_order: number
  stock: number
  created_at: string
}

export interface ProductPayload {
  name: string
  description: string | null
  price: string
  unit: string | null
  image_url: string | null
  is_active: boolean
  stock: number
}

export type PlantingStage = 'shade' | 'light' | 'ready'

export interface Planting {
  id: number
  product_id: number | null
  culture: string
  sown_at: string
  grow_days: number
  shade_days: number
  trays: number
  note: string | null
  ready_at: string
  stage: PlantingStage
  harvested_at: string | null
  harvested_qty: number | null
}

export interface HarvestPayload {
  product_id: number
  qty: number
}

export interface PlantingPayload {
  culture: string
  sown_at: string
  grow_days: number
  shade_days: number
  trays: number
  note?: string | null
  product_id?: number | null
}
