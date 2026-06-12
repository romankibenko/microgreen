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

export interface Planting {
  id: number
  product_id: number | null
  culture: string
  sown_at: string
  grow_days: number
  note: string | null
  ready_at: string
}

export interface PlantingPayload {
  culture: string
  sown_at: string
  grow_days: number
  note?: string | null
  product_id?: number | null
}
