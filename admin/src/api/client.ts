import axios from 'axios'

import { API_URL, TOKEN_KEY } from '@/config'
import type {
  HarvestPayload,
  Order,
  OrderStatus,
  Planting,
  PlantingPayload,
  Product,
  ProductPayload,
} from './types'

const api = axios.create({ baseURL: API_URL })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Протух/невалиден токен → выкидываем на логин.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY)
      if (location.pathname !== '/login') location.assign('/login')
    }
    return Promise.reject(error)
  },
)

export async function login(username: string, password: string): Promise<string> {
  const { data } = await api.post<{ access_token: string }>('/auth/login', {
    username,
    password,
  })
  return data.access_token
}

export async function fetchOrders(): Promise<Order[]> {
  const { data } = await api.get<Order[]>('/admin/orders')
  return data
}

export async function setOrderStatus(
  id: number,
  status: OrderStatus,
): Promise<Order> {
  const { data } = await api.patch<Order>(`/admin/orders/${id}/status`, { status })
  return data
}

export async function fetchProducts(): Promise<Product[]> {
  const { data } = await api.get<Product[]>('/admin/products')
  return data
}

export async function createProduct(payload: ProductPayload): Promise<Product> {
  const { data } = await api.post<Product>('/admin/products', payload)
  return data
}

export async function updateProduct(
  id: number,
  payload: Partial<ProductPayload>,
): Promise<Product> {
  const { data } = await api.patch<Product>(`/admin/products/${id}`, payload)
  return data
}

export async function deleteProduct(id: number): Promise<void> {
  await api.delete(`/admin/products/${id}`)
}

export async function fetchPlantings(): Promise<Planting[]> {
  const { data } = await api.get<Planting[]>('/admin/plantings')
  return data
}

export async function createPlanting(payload: PlantingPayload): Promise<Planting> {
  const { data } = await api.post<Planting>('/admin/plantings', payload)
  return data
}

export async function updatePlantingNote(
  id: number,
  note: string | null,
): Promise<Planting> {
  const { data } = await api.patch<Planting>(`/admin/plantings/${id}`, { note })
  return data
}

export async function harvestPlanting(
  id: number,
  payload: HarvestPayload,
): Promise<Planting> {
  const { data } = await api.post<Planting>(`/admin/plantings/${id}/harvest`, payload)
  return data
}

export async function deletePlanting(id: number): Promise<void> {
  await api.delete(`/admin/plantings/${id}`)
}
