import axios from 'axios'

import { API_URL, TOKEN_KEY } from '@/config'
import type { Order, OrderStatus, Planting, PlantingPayload } from './types'

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

export async function fetchPlantings(): Promise<Planting[]> {
  const { data } = await api.get<Planting[]>('/admin/plantings')
  return data
}

export async function createPlanting(payload: PlantingPayload): Promise<Planting> {
  const { data } = await api.post<Planting>('/admin/plantings', payload)
  return data
}

export async function deletePlanting(id: number): Promise<void> {
  await api.delete(`/admin/plantings/${id}`)
}
