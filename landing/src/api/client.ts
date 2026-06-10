import axios from 'axios'

import type { Order, OrderPayload, Product } from './types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})

export async function fetchProducts(): Promise<Product[]> {
  const { data } = await api.get<Product[]>('/products')
  return data
}

export async function createOrder(payload: OrderPayload): Promise<Order> {
  const { data } = await api.post<Order>('/orders', payload)
  return data
}
