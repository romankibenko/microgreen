export interface Product {
  id: number
  name: string
  description: string | null
  price: string
  unit: string | null
  image_url: string | null
  is_active: boolean
  created_at: string
}

export interface OrderItemPayload {
  product_id: number
  quantity: number
}

export interface OrderPayload {
  customer_phone: string
  customer_name?: string | null
  comment?: string | null
  items: OrderItemPayload[]
}

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
  status: string
  total: string
  created_at: string
  items: OrderItem[]
}
